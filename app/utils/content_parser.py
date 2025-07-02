import re
import json
import os
import shutil
from typing import Optional, List, Tuple
from pathlib import Path
from urllib.parse import urlparse

from app.utils.logger import get_logger

logger = get_logger("content_parser")


def parse_markdown_to_plain_text(content: str, max_length: int = 200) -> str:
    """
    Markdown 형식의 텍스트를 평문으로 변환

    Args:
        content: Markdown 형식의 텍스트
        max_length: 최대 길이 (기본값: 200)

    Returns:
        평문으로 변환된 텍스트
    """
    if not content:
        return ""

    # Markdown 문법 제거
    # 헤더 제거 (# ## ### 등)
    content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)

    # 볼드 제거 (**text** 또는 __text__)
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
    content = re.sub(r'__(.*?)__', r'\1', content)

    # 이탤릭 제거 (*text* 또는 _text_)
    content = re.sub(r'\*(.*?)\*', r'\1', content)
    content = re.sub(r'_(.*?)_', r'\1', content)

    # 코드 블록 제거 (```code```)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # 인라인 코드 제거 (`code`)
    content = re.sub(r'`(.*?)`', r'\1', content)

    # 링크 제거 ([text](url))
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # 이미지 제거 (![alt](url))
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', content)

    # 리스트 마커 제거 (- * + 1. 2. 등)
    content = re.sub(r'^[\s]*[-*+]\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'^[\s]*\d+\.\s+', '', content, flags=re.MULTILINE)

    # 인용 제거 (> text)
    content = re.sub(r'^>\s+', '', content, flags=re.MULTILINE)

    # 수평선 제거 (---, ***, ___)
    content = re.sub(r'^[-*_]{3,}$', '', content, flags=re.MULTILINE)

    # 줄바꿈을 공백으로 변환
    content = re.sub(r'\n+', ' ', content)

    # 연속된 공백을 하나로 변환
    content = re.sub(r'\s+', ' ', content)

    # 앞뒤 공백 제거
    content = content.strip()

    # 길이 제한
    if len(content) > max_length:
        content = content[:max_length].rsplit(' ', 1)[0] + '...'

    return content


def parse_quill_to_plain_text(content: str, max_length: int = 200) -> str:
    """
    Quill 에디터 형식의 텍스트를 평문으로 변환

    Args:
        content: Quill 형식의 JSON 문자열 또는 dict
        max_length: 최대 길이 (기본값: 200)

    Returns:
        평문으로 변환된 텍스트
    """
    if not content:
        return ""

    try:
        # JSON 문자열인 경우 파싱
        if isinstance(content, str):
            quill_data = json.loads(content)
        else:
            quill_data = content

        # Quill 형식 확인
        if not isinstance(quill_data, dict) or 'ops' not in quill_data:
            # 일반 텍스트로 처리
            return parse_markdown_to_plain_text(content, max_length)

        plain_text = ""

        for op in quill_data.get('ops', []):
            if 'insert' in op:
                insert_data = op['insert']

                if isinstance(insert_data, str):
                    # 일반 텍스트
                    plain_text += insert_data
                elif isinstance(insert_data, dict):
                    # 이미지나 다른 객체
                    if 'image' in insert_data:
                        # 이미지 alt 텍스트가 있으면 추가
                        alt_text = insert_data.get('alt', '')
                        if alt_text:
                            plain_text += f" {alt_text} "

        # 줄바꿈을 공백으로 변환
        plain_text = re.sub(r'\n+', ' ', plain_text)

        # 연속된 공백을 하나로 변환
        plain_text = re.sub(r'\s+', ' ', plain_text)

        # 앞뒤 공백 제거
        plain_text = plain_text.strip()

        # 길이 제한
        if len(plain_text) > max_length:
            plain_text = plain_text[:max_length].rsplit(' ', 1)[0] + '...'

        return plain_text

    except (json.JSONDecodeError, KeyError, TypeError):
        # JSON 파싱 실패 시 일반 텍스트로 처리
        return parse_markdown_to_plain_text(content, max_length)


def parse_content_to_plain_text(content: str, content_type: str = "markdown", max_length: int = 200) -> str:
    """
    content를 평문으로 변환하는 통합 함수

    Args:
        content: 원본 content
        content_type: content 타입 ("markdown", "quill", "plain")
        max_length: 최대 길이 (기본값: 200)

    Returns:
        평문으로 변환된 텍스트
    """
    if not content:
        return ""

    if content_type.lower() == "quill":
        return parse_quill_to_plain_text(content, max_length)
    elif content_type.lower() == "markdown":
        return parse_markdown_to_plain_text(content, max_length)
    else:
        # plain text인 경우 단순 길이 제한만
        content = content.strip()
        if len(content) > max_length:
            content = content[:max_length].rsplit(' ', 1)[0] + '...'
        return content


def extract_images_from_markdown(content: str) -> List[Tuple[str, str, str]]:
    """
    Markdown에서 이미지 URL을 추출

    Args:
        content: Markdown 형식의 텍스트

    Returns:
        List of (alt_text, image_url, full_match) tuples
    """
    if not content:
        return []

    # ![alt](url) 패턴 찾기
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)

    return [(alt.strip(), url.strip(), f'![{alt}]({url})') for alt, url in matches]


def extract_images_from_quill(content: str) -> List[Tuple[str, str, dict]]:
    """
    Quill에서 이미지 URL을 추출

    Args:
        content: Quill 형식의 JSON 문자열

    Returns:
        List of (alt_text, image_url, op_data) tuples
    """
    if not content:
        return []

    try:
        if isinstance(content, str):
            quill_data = json.loads(content)
        else:
            quill_data = content

        if not isinstance(quill_data, dict) or 'ops' not in quill_data:
            return []

        images = []
        for op in quill_data.get('ops', []):
            if 'insert' in op and isinstance(op['insert'], dict):
                insert_data = op['insert']
                if 'image' in insert_data:
                    image_url = insert_data['image']
                    alt_text = insert_data.get('alt', '')
                    images.append((alt_text, image_url, op))

        return images

    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def extract_images_from_content(content: str, content_type: str = "markdown") -> List[Tuple[str, str]]:
    """
    content에서 이미지 URL을 추출하는 통합 함수

    Args:
        content: 원본 content
        content_type: content 타입 ("markdown", "quill", "plain")

    Returns:
        List of (alt_text, image_url) tuples
    """
    if not content:
        return []

    if content_type.lower() == "quill":
        images = extract_images_from_quill(content)
        return [(alt, url) for alt, url, _ in images]
    elif content_type.lower() == "markdown":
        images = extract_images_from_markdown(content)
        return [(alt, url) for alt, url, _ in images]
    else:
        return []


def is_temp_image_url(url: str, temp_path: str = "./temp") -> bool:
    """
    URL이 임시 이미지 경로인지 확인 (S3/Local 호환)

    Args:
        url: 이미지 URL
        temp_path: 임시 파일 경로

    Returns:
        임시 이미지 여부
    """
    if not url:
        return False

    logger.debug(f"Checking if URL is temp: {url}")

    # 외부 URL인 경우 (http, https)
    try:
        parsed = urlparse(url)
        if parsed.scheme in ['http', 'https']:
            # S3 URL에서 temp 키워드 확인
            if 'temp' in parsed.path.lower() or 'temp' in parsed.netloc.lower():
                logger.debug(f"URL is temp (HTTP): {url}")
                return True
            logger.debug(f"URL is not temp (HTTP): {url}")
            return False
    except:
        pass

    # 로컬 파일 경로인 경우
    if url.startswith('./') or url.startswith('/') or url.startswith('temp/'):
        result = temp_path in url or 'temp' in url.lower()
        logger.debug(f"URL is temp (local): {url} -> {result}")
        return result

    # 상대 경로인 경우
    if not url.startswith('http'):
        result = 'temp' in url.lower()
        logger.debug(f"URL is temp (relative): {url} -> {result}")
        return result

    logger.debug(f"URL is not temp: {url}")
    return False


def get_temp_path_from_url(url: str, temp_path: str = "./temp") -> Optional[str]:
    """
    URL에서 임시 파일 경로 추출

    Args:
        url: 이미지 URL
        temp_path: 임시 파일 기본 경로

    Returns:
        임시 파일 경로 (없으면 None)
    """
    if not is_temp_image_url(url, temp_path):
        return None

    logger.debug(f"Extracting temp path from URL: {url}")

    try:
        parsed = urlparse(url)
        if parsed.scheme in ['http', 'https']:
            # S3 URL인 경우
            path_parts = parsed.path.strip('/').split('/')
            if 'temp' in path_parts:
                temp_index = path_parts.index('temp')
                result = '/'.join(path_parts[temp_index:])
                logger.debug(f"Extracted temp path (HTTP): {result}")
                return result
        else:
            # 로컬 파일 경로인 경우
            if url.startswith('./temp/'):
                result = url[7:]  # ./temp/ 제거
                logger.debug(f"Extracted temp path (./temp/): {result}")
                return result
            elif url.startswith('./'):
                result = url[2:]  # ./ 제거
                logger.debug(f"Extracted temp path (./): {result}")
                return result
            elif url.startswith('/temp/'):
                result = url[6:]  # /temp/ 제거
                logger.debug(f"Extracted temp path (/temp/): {result}")
                return result
            elif url.startswith('/'):
                result = url[1:]  # / 제거
                logger.debug(f"Extracted temp path (/): {result}")
                return result
            else:
                logger.debug(f"Extracted temp path (as-is): {url}")
                return url
    except Exception as e:
        logger.error(f"Error extracting temp path from {url}: {e}")
        pass

    return None


def move_temp_images_to_storage(content: str, content_type: str, post_id: str,
                                temp_path: str = "./temp",
                                storage_path: str = "./uploads/posts") -> Tuple[str, List[str]]:
    """
    content의 임시 이미지들을 실제 저장소로 이동

    Args:
        content: 원본 content
        content_type: content 타입
        post_id: 게시글 ID
        temp_path: 임시 파일 경로
        storage_path: 저장소 경로

    Returns:
        (업데이트된 content, 이동된 파일 경로 리스트)
    """
    if not content:
        logger.debug("No content provided, skipping image move")
        return content, []

    logger.info(f"Starting image move for post {post_id}")
    logger.debug(f"Temp path: {temp_path}, Storage path: {storage_path}")
    logger.debug(f"Content type: {content_type}")

    moved_files = []
    updated_content = content

    # 이미지 추출
    images = extract_images_from_content(content, content_type)
    logger.info(f"Found {len(images)} images in content")

    for i, (alt_text, image_url) in enumerate(images):
        logger.debug(f"Processing image {i+1}: {image_url}")
        
        if is_temp_image_url(image_url, temp_path):
            logger.info(f"Moving temp image: {image_url}")
            
            # 임시 파일 경로에서 실제 파일명 추출
            temp_file_path = get_temp_path_from_url(image_url, temp_path)
            if not temp_file_path:
                logger.warning(f"Could not extract temp path from {image_url}")
                continue

            file_name = os.path.basename(temp_file_path)
            logger.debug(f"File name: {file_name}")

            # 임시 파일 전체 경로
            full_temp_path = os.path.join(temp_path, temp_file_path)
            logger.debug(f"Full temp path: {full_temp_path}")

            # 저장소 파일 경로 (게시글별 폴더)
            storage_file_path = os.path.join(storage_path, post_id, file_name)
            logger.debug(f"Storage file path: {storage_file_path}")

            # 저장소 디렉토리 생성
            storage_dir = os.path.dirname(storage_file_path)
            logger.debug(f"Creating storage directory: {storage_dir}")
            os.makedirs(storage_dir, exist_ok=True)

            # 파일 이동
            if os.path.exists(full_temp_path):
                logger.info(f"Moving file from {full_temp_path} to {storage_file_path}")
                try:
                    shutil.move(full_temp_path, storage_file_path)
                    moved_files.append(storage_file_path)
                    logger.info(f"Successfully moved file: {storage_file_path}")

                    # content에서 URL 업데이트
                    new_url = f"/uploads/posts/{post_id}/{file_name}"
                    logger.debug(f"Updating URL from {image_url} to {new_url}")
                    
                    if content_type.lower() == "markdown":
                        # Markdown: ![alt](old_url) -> ![alt](new_url)
                        pattern = rf'!\[{re.escape(alt_text)}\]\({re.escape(image_url)}\)'
                        replacement = f'![{alt_text}]({new_url})'
                        updated_content = re.sub(pattern, replacement, updated_content)
                        logger.debug(f"Updated markdown content")
                    elif content_type.lower() == "quill":
                        # Quill: JSON 내의 image URL 업데이트
                        try:
                            quill_data = json.loads(updated_content)
                            for op in quill_data.get('ops', []):
                                if 'insert' in op and isinstance(op['insert'], dict):
                                    if 'image' in op['insert'] and op['insert']['image'] == image_url:
                                        op['insert']['image'] = new_url
                            updated_content = json.dumps(quill_data)
                            logger.debug(f"Updated quill content")
                        except Exception as e:
                            logger.error(f"Error updating quill content: {e}")
                            pass  # JSON 파싱 실패 시 무시
                except Exception as e:
                    logger.error(f"Error moving file from {full_temp_path} to {storage_file_path}: {e}")
            else:
                logger.warning(f"Temp file does not exist: {full_temp_path}")
        else:
            logger.debug(f"Image is not temp, skipping: {image_url}")

    logger.info(f"Image move completed. Moved {len(moved_files)} files")
    return updated_content, moved_files


def cleanup_temp_images(content: str, content_type: str, temp_path: str = "./temp") -> List[str]:
    """
    content에서 사용되지 않는 임시 이미지들을 정리

    Args:
        content: 원본 content
        content_type: content 타입
        temp_path: 임시 파일 경로

    Returns:
        삭제된 파일 경로 리스트
    """
    if not content:
        return []

    deleted_files = []

    # content에서 사용되는 이미지 URL 추출
    used_images = extract_images_from_content(content, content_type)
    used_urls = {url for _, url in used_images}

    # 임시 디렉토리의 모든 파일 확인
    if os.path.exists(temp_path):
        for root, dirs, files in os.walk(temp_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # 상대 경로로 변환
                rel_path = os.path.relpath(file_path, temp_path)
                file_url = f"./temp/{rel_path}"

                # 파일이 content에서 사용되지 않으면 삭제
                if file_url not in used_urls:
                    try:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                    except:
                        pass  # 삭제 실패 시 무시

    return deleted_files


def extract_embedded_images_from_content(content: str, content_type: str = "markdown") -> List[str]:
    """
    content에서 임베딩된 이미지 URL 목록을 추출하여 JSON 형태로 반환

    Args:
        content: 원본 content
        content_type: content 타입

    Returns:
        이미지 URL 목록 (JSON 문자열)
    """
    if not content:
        return []

    images = extract_images_from_content(content, content_type)
    image_urls = [url for _, url in images]

    return image_urls
