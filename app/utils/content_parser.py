import re
import json
from typing import Optional


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