from crewai import Agent
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Initialize Gemini LLM
def get_gemini_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )

class NewsGroupAgents:
    def __init__(self):
        self.llm = get_gemini_llm()
    
    def spamfilter_agent(self):
        return Agent(
            role="Spam Filter Expert",
            goal="Analyze text content to identify spam, advertisements, newsletters, and inappropriate content.",
            backstory="""You are an expert spam filter with years of experience analyzing online content. 
            You have a keen eye for identifying advertisements, promotional content, newsletters, and vulgar language. 
            You take pride in maintaining clean, appropriate discussion spaces.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def analyst_agent(self):
        return Agent(
            role="Discussion Analyst",
            goal="Extract and organize key arguments and positions from discussion participants while preserving the essence of their contributions.",
            backstory="""You are an expert discussion analyst with expertise in identifying different voices 
            and perspectives in conversations. You excel at distilling complex discussions into clear, 
            organized summaries while maintaining the integrity of each participant's viewpoint.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def scriptwriter_agent(self):
        return Agent(
            role="Script Writer",
            goal="Transform analyzed discussions into natural, engaging movie-style dialogue that captures the essence of the conversation.",
            backstory="""You are a professional scriptwriter with expertise in creating natural, 
            flowing dialogue for films. You focus purely on spoken words and avoid any stage directions, 
            actions, or parentheticals. Your dialogue sounds authentic and engaging.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def formatter_agent(self):
        return Agent(
            role="Text Formatter",
            goal="Clean and format text to professional standards, removing unwanted elements while maintaining readability.",
            backstory="""You are a meticulous text formatter with an eye for clean, professional presentation. 
            You excel at removing extraneous elements like stage directions and formatting artifacts 
            while preserving the core content.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def scorer_agent(self):
        return Agent(
            role="Dialogue Quality Assessor",
            goal="""Evaluate dialogue quality on a 1-10 scale across multiple dimensions:
            
            SCORING CRITERIA:
            • Clarity (1-10): How clear and understandable is the exchange?
            • Relevance (1-10): Do responses stay on topic and contribute meaningfully?
            • Conciseness (1-10): Is the dialogue free of unnecessary redundancy?
            • Politeness (1-10): Are participants respectful and considerate?
            • Engagement (1-10): Do participants seem interested and involved?
            • Flow (1-10): Is there natural progression without awkward transitions?
            • Coherence (1-10): Does the dialogue make logical sense overall?
            • Responsiveness (1-10): Do participants address each other's points adequately?
            • Language Use (1-10): Is grammar, vocabulary, and syntax appropriate?
            • Emotional Intelligence (1-10): Are participants sensitive to emotional tone?
            
            SCALE INTERPRETATION:
            1-3: Poor - Significant issues preventing effective communication
            4-6: Average - Some good points but notable weaknesses
            7-9: Good - Mostly effective with minor issues
            10: Excellent - Exemplary with no apparent issues""",
            backstory="""You are an expert dialogue assessor with extensive experience evaluating 
            conversational quality across multiple dimensions. You have a keen analytical mind and 
            can identify both strengths and areas for improvement in any dialogue exchange.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )