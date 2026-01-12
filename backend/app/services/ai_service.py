"""
AI Service for content analysis and adaptation
"""
from typing import List, Optional, Dict, Any
import json
from openai import AsyncOpenAI
import anthropic

from ..core.config import settings
from ..models.content import Platform, ContentType
from ..schemas.content import PLATFORM_CONFIGS, ContentAnalysis, AdaptationPreview


class AIService:
    """Service for AI-powered content processing"""

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None
        self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY) if settings.ANTHROPIC_API_KEY else None

    async def analyze_content(
        self,
        content_text: str,
        content_type: ContentType,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContentAnalysis:
        """Analyze content to extract key information and style fingerprint"""

        prompt = f"""
        分析以下{content_type.value}内容，提取关键信息：

        内容：
        {content_text[:5000]}  # Limit to 5000 chars

        请以JSON格式返回以下信息：
        1. key_points: 3-5个核心观点/信息点
        2. emotional_tone: 情感基调（专业/幽默/亲切/严肃/轻松）
        3. main_topics: 主要话题标签
        4. visual_elements: 视觉元素描述（如有）
        5. style_fingerprint: 风格指纹
           - language_style: 语言风格
           - visual_style: 视觉风格（如适用）
           - pace: 节奏感（快/中/慢）
        """

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "你是一个专业的内容分析师，擅长分析自媒体内容的风格和特点。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
        else:
            # Fallback mock response for development
            result = {
                "key_points": ["核心观点1", "核心观点2", "核心观点3"],
                "emotional_tone": "专业",
                "main_topics": ["科技", "教程"],
                "visual_elements": ["人物出镜", "图表展示"],
                "style_fingerprint": {
                    "language_style": "专业",
                    "visual_style": "简约",
                    "pace": "中等"
                }
            }

        return ContentAnalysis(**result)

    async def generate_adaptation(
        self,
        original_content: str,
        analysis: ContentAnalysis,
        target_platform: Platform,
        preserve_style: bool = True
    ) -> AdaptationPreview:
        """Generate content adaptation for target platform"""

        platform_config = PLATFORM_CONFIGS[target_platform]

        prompt = f"""
        将以下内容适配到{platform_config.display_name}平台：

        原始内容：
        {original_content[:3000]}

        内容分析：
        - 核心观点：{', '.join(analysis.key_points)}
        - 情感基调：{analysis.emotional_tone}
        - 主要话题：{', '.join(analysis.main_topics)}

        平台特性：
        - 标题长度限制：{platform_config.max_title_length}字
        - 文案长度限制：{platform_config.max_caption_length}字
        - 风格关键词：{', '.join(platform_config.style_keywords)}

        请生成：
        1. suggested_title: 适合该平台的标题（符合长度限制）
        2. suggested_caption: 适合该平台的文案/描述
        3. suggested_hashtags: 5-10个相关话题标签
        4. content_outline: 内容大纲（用于视频剪辑/文章改写）

        要求：
        - {'保持原有风格特点' if preserve_style else '完全适配平台风格'}
        - 使用{platform_config.display_name}平台的流行表达方式
        - 标题要有吸引力，符合平台用户偏好
        """

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": f"你是一个专业的{platform_config.display_name}内容运营专家。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
        else:
            # Fallback mock response
            result = {
                "suggested_title": f"【必看】{analysis.key_points[0] if analysis.key_points else '精彩内容'}",
                "suggested_caption": f"分享一个关于{', '.join(analysis.main_topics[:2]) if analysis.main_topics else '精彩话题'}的内容...",
                "suggested_hashtags": [f"#{topic}" for topic in analysis.main_topics[:5]] if analysis.main_topics else ["#干货", "#分享"],
                "content_outline": ["开头引入", "核心内容", "总结收尾"]
            }

        return AdaptationPreview(
            platform=target_platform,
            platform_config=platform_config,
            suggested_title=result.get("suggested_title", ""),
            suggested_caption=result.get("suggested_caption", ""),
            suggested_hashtags=result.get("suggested_hashtags", []),
            thumbnail_preview_url=None,
            estimated_duration_seconds=None
        )

    async def rewrite_text(
        self,
        text: str,
        target_platform: Platform,
        style: Optional[str] = None
    ) -> str:
        """Rewrite text for specific platform style"""

        platform_config = PLATFORM_CONFIGS[target_platform]

        prompt = f"""
        将以下文本改写为适合{platform_config.display_name}的风格：

        原文：
        {text}

        要求：
        - 使用{platform_config.display_name}的流行表达方式
        - 风格关键词：{', '.join(platform_config.style_keywords)}
        - {f'额外风格要求：{style}' if style else ''}
        - 保持原意，但改变表达方式
        - 长度控制在{platform_config.max_caption_length or 1000}字以内

        直接输出改写后的文本，不要有任何解释。
        """

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "你是一个专业的文案撰写专家。"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        else:
            return text  # Return original if no AI available

    async def generate_titles(
        self,
        content: str,
        target_platform: Platform,
        count: int = 5
    ) -> List[str]:
        """Generate multiple title options for A/B testing"""

        platform_config = PLATFORM_CONFIGS[target_platform]

        prompt = f"""
        为以下内容生成{count}个不同风格的{platform_config.display_name}标题：

        内容摘要：
        {content[:1000]}

        要求：
        - 每个标题长度不超过{platform_config.max_title_length}字
        - 风格多样：包括悬念式、数字式、提问式、利益式等
        - 符合{platform_config.display_name}平台用户偏好

        以JSON数组格式返回标题列表。
        """

        if self.openai_client:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "你是一个标题创作专家。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            result = json.loads(response.choices[0].message.content)
            return result.get("titles", [])
        else:
            return [
                "【必看】这个内容太精彩了！",
                "3分钟带你了解全部要点",
                "你知道吗？这个方法改变了一切",
                "90%的人都不知道的技巧",
                "这可能是今年最值得看的内容"
            ][:count]


# Create singleton instance
ai_service = AIService()
