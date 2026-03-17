"""
파서 모듈
HTML 파싱 및 게시글 데이터 추출
"""
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from src.logger import Logger


class Post:
    """게시글 데이터 클래스"""
    
    def __init__(self, post_id: str, title: str, link: str):
        """
        게시글 초기화
        
        Args:
            post_id: 게시글 ID
            title: 게시글 제목
            link: 게시글 링크
        """
        self.id = post_id
        self.title = title
        self.link = link
    
    def to_dict(self) -> Dict[str, str]:
        """게시글을 딕셔너리로 변환"""
        return {'id': self.id, 'title': self.title, 'link': self.link}
    
    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title})"


class Parser:
    """HTML 파서 클래스"""
    
    def __init__(self, base_url: str = "https://gall.dcinside.com"):
        """
        파서 초기화
        
        Args:
            base_url: 상대 경로를 절대 경로로 변환할 기본 URL
        """
        self.base_url = base_url
        self.logger = Logger.get_logger()
    
    def parse_posts(
        self,
        html_content: Optional[str],
        post_selector: str,
        title_selector: str,
        link_selector: str,
        id_selector: str
    ) -> List[Post]:
        """
        HTML 내용에서 게시글 추출
        
        Args:
            html_content: HTML 문자열
            post_selector: 게시글 요소 CSS Selector
            title_selector: 제목 요소 CSS Selector
            link_selector: 링크 요소 CSS Selector
            id_selector: ID 요소 CSS Selector
            
        Returns:
            Post 객체 리스트
        """
        if not html_content:
            self.logger.warning("HTML 내용이 없습니다.")
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            posts = []
            
            for post_element in soup.select(post_selector):
                try:
                    post = self._extract_post(
                        post_element,
                        title_selector,
                        link_selector,
                        id_selector
                    )
                    if post:
                        posts.append(post)
                except Exception as e:
                    self.logger.debug(f"게시글 파싱 오류: {e}")
                    continue
            
            self.logger.debug(f"총 {len(posts)}개의 게시글을 파싱했습니다.")
            return posts
        except Exception as e:
            self.logger.error(f"HTML 파싱 중 오류: {e}")
            return []
    
    def _extract_post(
        self,
        post_element,
        title_selector: str,
        link_selector: str,
        id_selector: str
    ) -> Optional[Post]:
        """
        개별 게시글 요소에서 정보 추출
        
        Args:
            post_element: BeautifulSoup Post 요소
            title_selector: 제목 CSS Selector
            link_selector: 링크 CSS Selector
            id_selector: ID CSS Selector
            
        Returns:
            Post 객체 또는 None
        """
        # ID 추출 및 검증
        id_element = post_element.select_one(id_selector)
        if not id_element:
            return None
        
        post_id = id_element.get_text(strip=True)
        
        # ID가 숫자인지 확인 (일반 게시글 필터링)
        if not post_id.isdigit():
            return None
        
        # 제목 추출
        title_element = post_element.select_one(title_selector)
        if not title_element:
            return None
        
        title = title_element.get_text(strip=True)
        if not title:
            return None
        
        # 링크 추출 및 절대 경로 변환
        link_element = post_element.select_one(link_selector)
        if not link_element or 'href' not in link_element.attrs:
            return None
        
        link = link_element['href']
        if not link.startswith('http'):
            link = self.base_url + link
        
        return Post(post_id, title, link)
