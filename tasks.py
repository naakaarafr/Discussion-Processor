from crewai import Task

class NewsGroupTasks:
    def __init__(self, discussion_content):
        self.discussion_content = discussion_content
    
    def spam_filter_task(self, agent):
        return Task(
            description=f"""
            Analyze the following text to determine if it contains spam, advertisements, 
            newsletters, or inappropriate/vulgar language.
            
            TEXT TO ANALYZE:
            {self.discussion_content}
            
            EVALUATION CRITERIA:
            - Spam: Unsolicited promotional content, repetitive messaging
            - Advertisements: Product promotions, sales pitches, marketing content
            - Newsletters: Formatted email-style announcements or updates
            - Vulgar Language: Offensive, inappropriate, or profane content
            - Inappropriate Content: Harmful, discriminatory, or offensive material
            
            RESPONSE FORMAT:
            - If content is problematic: Start with "STOP" followed by specific reasoning
            - If content is acceptable: Start with "PASS" followed by brief explanation
            """,
            expected_output="Either 'STOP' or 'PASS' followed by clear reasoning for the decision",
            agent=agent
        )
    
    def analysis_task(self, agent):
        return Task(
            description=f"""
            Analyze the following discussion text and extract key information about each participant's contributions.
            
            DISCUSSION CONTENT:
            {self.discussion_content}
            
            YOUR TASK:
            1. Identify all discussion participants (speakers/contributors)
            2. Extract the main arguments, points, or positions of each participant
            3. Organize the information clearly, showing who said what
            4. You may rephrase or reword statements for clarity, but preserve the core meaning
            5. Maintain the logical flow and context of the discussion
            
            FOCUS ON:
            - Key arguments and positions
            - Main discussion topics
            - Different perspectives presented
            - Important facts or claims made
            """,
            expected_output="A structured analysis clearly identifying each participant's arguments and main discussion points, with appropriate rewording while preserving core meanings",
            agent=agent
        )
    
    def scriptwriting_task(self, agent):
        return Task(
            description="""
            Transform the analyzed conversation into a natural movie script dialogue format.
            
            STRICT REQUIREMENTS:
            ✓ INCLUDE: Only spoken dialogue text
            ✓ FOCUS: Natural, conversational flow
            ✓ FORMAT: Standard script format with speaker names
            
            ✗ EXCLUDE: 
            - Stage directions or actions
            - Parentheticals like (smiling), (angry), etc.
            - Situational descriptions
            - Camera directions
            - Scene settings
            - Character descriptions
            
            EXAMPLE FORMAT:
            SPEAKER1: [Their dialogue here]
            SPEAKER2: [Their response here]
            
            Make the dialogue sound natural and engaging while preserving the original discussion's essence.
            """,
            expected_output="Clean movie script dialogue with only speaker names and spoken text, no stage directions, actions, or parentheticals",
            agent=agent
        )
    
    def formatting_task(self, agent):
        return Task(
            description="""
            Clean and format the dialogue text to professional standards.
            
            FORMATTING REQUIREMENTS:
            1. Remove all bracketed actions: [nodding], [gesturing], etc.
            2. Remove all parenthetical actions: (smiling), (laughing), etc.
            3. Clean up inconsistent spacing and line breaks
            4. Ensure consistent speaker name formatting
            5. Remove any remaining formatting artifacts
            6. Maintain proper dialogue structure
            7. Ensure professional, readable presentation
            
            PRESERVE:
            - All actual dialogue content
            - Speaker identifications
            - Logical conversation flow
            - Paragraph structure where appropriate
            """,
            expected_output="Professionally formatted, clean dialogue text with all bracketed/parenthetical actions removed and consistent formatting throughout",
            agent=agent
        )
    
    def scoring_task(self, agent, dialogue_result):
        return Task(
            description=f"""
            Evaluate the quality of the following dialogue transformation using your established criteria.
            
            DIALOGUE TO SCORE:
            {dialogue_result}
            
            EVALUATION PROCESS:
            1. Assess each of the 10 criteria mentioned in your goal (Clarity, Relevance, Conciseness, etc.)
            2. Consider the overall effectiveness of the dialogue
            3. Provide a comprehensive score from 1-10
            
            RESPONSE FORMAT:
            - First line: Only the numerical score (1-10)
            - Subsequent lines: Brief explanation of the score, highlighting key strengths and areas for improvement
            
            EXAMPLE:
            8
            The dialogue demonstrates strong clarity and natural flow, with good engagement between participants. 
            Minor improvements could be made in conciseness, but overall it effectively captures the original discussion.
            """,
            expected_output="A numerical score (1-10) on the first line, followed by a brief explanation of the scoring rationale",
            agent=agent
        )