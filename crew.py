from crewai import Crew, Process
from agents import NewsGroupAgents
from tasks import NewsGroupTasks
from tools import TextProcessor, LoggingTools, ValidationTools, FileManager
from typing import Dict, Any, Optional

class NewsGroupCrew:
    def __init__(self, discussion_content: str):
        self.discussion_content = discussion_content
        self.agents = None
        self.tasks = None
        self.text_processor = TextProcessor()
        self.file_manager = FileManager()
        
        # Initialize agents and tasks with error handling
        try:
            self.agents = NewsGroupAgents()
            self.tasks = NewsGroupTasks(discussion_content)
            LoggingTools.log_step("INITIALIZATION", "NewsGroupCrew initialized successfully")
        except Exception as e:
            LoggingTools.log_error(f"Failed to initialize crew: {str(e)}", "Initialization")
            raise
    
    def run_spam_filter(self) -> bool:
        """Run spam filter check and return True if content should be processed"""
        LoggingTools.log_step("SPAM FILTER", "Checking for spam and inappropriate content")
        
        try:
            spamfilter_agent = self.agents.spamfilter_agent()
            spam_task = self.tasks.spam_filter_task(spamfilter_agent)
            
            LoggingTools.log_step("SPAM FILTER EXECUTION", "Running spam filter analysis")
            result = spam_task.execute()
            
            if not ValidationTools.validate_agent_response(str(result), "Spam Filter Agent"):
                LoggingTools.log_error("Spam filter returned invalid response", "Spam Filter")
                return False
            
            result_str = str(result).upper()
            LoggingTools.log_result("Spam Filter Result", str(result))
            
            if "STOP" in result_str:
                print("❌ Content filtered out by spam filter")
                LoggingTools.log_step("SPAM FILTER RESULT", "Content REJECTED - flagged as inappropriate")
                return False
            else:
                print("✅ Content passed spam filter")
                LoggingTools.log_step("SPAM FILTER RESULT", "Content APPROVED - safe to process")
                return True
                
        except Exception as e:
            LoggingTools.log_error(f"Error in spam filter: {str(e)}", "Spam Filter")
            print(f"❌ Spam filter error: {str(e)}")
            return False
    
    def run_dialogue_transformation(self) -> Optional[str]:
        """Run the main crew to transform discussion into dialogue"""
        LoggingTools.log_step("DIALOGUE TRANSFORMATION", "Starting crew processing pipeline")
        
        try:
            # Create agents
            LoggingTools.log_step("AGENT CREATION", "Initializing transformation agents")
            analyst = self.agents.analyst_agent()
            scriptwriter = self.agents.scriptwriter_agent()
            formatter = self.agents.formatter_agent()
            
            # Create tasks
            LoggingTools.log_step("TASK CREATION", "Setting up transformation tasks")
            analysis_task = self.tasks.analysis_task(analyst)
            script_task = self.tasks.scriptwriting_task(scriptwriter)
            format_task = self.tasks.formatting_task(formatter)
            
            # Create and run crew
            LoggingTools.log_step("CREW EXECUTION", "Running sequential processing crew")
            crew = Crew(
                agents=[analyst, scriptwriter, formatter],
                tasks=[analysis_task, script_task, format_task],
                verbose=2,
                process=Process.sequential
            )
            
            result = crew.kickoff()
            
            # Validate crew result
            if not ValidationTools.validate_crew_result(result):
                LoggingTools.log_error("Crew returned invalid result", "Dialogue Transformation")
                return None
            
            # Clean the result
            LoggingTools.log_step("RESULT CLEANING", "Cleaning and formatting final output")
            cleaned_result = self.text_processor.clean_dialogue(str(result))
            
            if not cleaned_result.strip():
                LoggingTools.log_error("Cleaned result is empty", "Dialogue Transformation")
                return None
            
            LoggingTools.log_result("Dialogue Transformation Result", cleaned_result)
            print("✅ Dialogue transformation completed successfully")
            
            return cleaned_result
            
        except Exception as e:
            LoggingTools.log_error(f"Error in dialogue transformation: {str(e)}", "Dialogue Transformation")
            print(f"❌ Dialogue transformation error: {str(e)}")
            return None
    
    def score_dialogue(self, dialogue_result: str) -> str:
        """Score the quality of the dialogue transformation"""
        LoggingTools.log_step("SCORING", "Evaluating dialogue quality")
        
        if not dialogue_result or not dialogue_result.strip():
            LoggingTools.log_error("Cannot score empty dialogue", "Scoring")
            return "0"
        
        try:
            scorer_agent = self.agents.scorer_agent()
            scoring_task = self.tasks.scoring_task(scorer_agent, dialogue_result)
            
            LoggingTools.log_step("SCORE EXECUTION", "Running quality assessment")
            score_result = scoring_task.execute()
            
            if not ValidationTools.validate_agent_response(str(score_result), "Scorer Agent"):
                LoggingTools.log_error("Scorer returned invalid response", "Scoring")
                return "0"
            
            score = self.text_processor.extract_score(str(score_result))
            
            LoggingTools.log_result("Scoring Result", f"Score: {score}/10\nDetails: {str(score_result)}")
            print(f"✅ Dialogue scored: {score}/10")
            
            return score
            
        except Exception as e:
            LoggingTools.log_error(f"Error in scoring: {str(e)}", "Scoring")
            print(f"❌ Scoring error: {str(e)}")
            return "0"
    
    def process_discussion(self, save_output: bool = True, save_logs: bool = True) -> Dict[str, Any]:
        """Complete processing pipeline for newsgroup discussion"""
        LoggingTools.clear_log()  # Start with fresh log
        LoggingTools.log_step("PIPELINE START", "Beginning complete discussion processing")
        
        # Validate environment
        LoggingTools.log_step("ENVIRONMENT CHECK", "Validating system requirements")
        if not ValidationTools.validate_environment():
            error_msg = "Environment validation failed - check API keys"
            LoggingTools.log_error(error_msg, "Environment")
            return {"error": error_msg}
        
        # Validate discussion content
        LoggingTools.log_step("CONTENT VALIDATION", "Checking discussion content quality")
        if not TextProcessor.validate_discussion_content(self.discussion_content):
            error_msg = "Invalid or insufficient discussion content (minimum 100 characters, meaningful content required)"
            LoggingTools.log_error(error_msg, "Content Validation")
            return {"error": error_msg}
        
        LoggingTools.log_result("Input Discussion Content", self.discussion_content, 300)
        
        try:
            # Step 1: Spam filter
            LoggingTools.log_step("STEP 1", "Spam and content filtering")
            if not self.run_spam_filter():
                result = {
                    "status": "filtered",
                    "message": "Content was filtered out by spam filter"
                }
                LoggingTools.log_result("Final Result", str(result))
                if save_logs:
                    LoggingTools.save_log_to_file(self.file_manager)
                return result
            
            # Step 2: Transform to dialogue
            LoggingTools.log_step("STEP 2", "Discussion to dialogue transformation")
            dialogue_result = self.run_dialogue_transformation()
            
            if not dialogue_result:
                error_msg = "Dialogue transformation failed - no output generated"
                LoggingTools.log_error(error_msg, "Processing Pipeline")
                if save_logs:
                    LoggingTools.save_log_to_file(self.file_manager)
                return {"error": error_msg}
            
            # Step 3: Score the result
            LoggingTools.log_step("STEP 3", "Quality assessment and scoring")
            score = self.score_dialogue(dialogue_result)
            
            # Save output if requested
            if save_output:
                LoggingTools.log_step("FILE OPERATIONS", "Saving results to files")
                
                # Save dialogue
                dialogue_saved = self.file_manager.save_result(dialogue_result, "dialogue_output.txt")
                
                # Save score with details
                score_content = f"Dialogue Quality Score: {score}/10\n\n"
                score_content += f"Generated on: {LoggingTools._log_buffer[0] if LoggingTools._log_buffer else 'Unknown'}\n\n"
                score_content += "DIALOGUE CONTENT:\n"
                score_content += "=" * 50 + "\n"
                score_content += dialogue_result
                
                score_saved = self.file_manager.save_result(score_content, "dialogue_score.txt")
                
                if not (dialogue_saved and score_saved):
                    LoggingTools.log_error("Some files failed to save", "File Operations")
            
            # Save logs if requested
            if save_logs:
                LoggingTools.save_log_to_file(self.file_manager)
            
            # Prepare final result
            result = {
                "status": "success",
                "dialogue": dialogue_result,
                "score": score,
                "message": f"Successfully processed discussion with score: {score}/10",
                "stats": {
                    "original_length": len(self.discussion_content),
                    "processed_length": len(dialogue_result),
                    "files_saved": save_output
                }
            }
            
            LoggingTools.log_step("PIPELINE COMPLETE", f"Processing successful - Score: {score}/10")
            LoggingTools.log_result("Final Result", str(result))
            
            return result
            
        except Exception as e:
            error_msg = f"Error during processing pipeline: {str(e)}"
            LoggingTools.log_error(error_msg, "Processing Pipeline")
            print(f"❌ {error_msg}")
            
            if save_logs:
                LoggingTools.save_log_to_file(self.file_manager)
            
            return {"error": error_msg}
    
    def process_from_file(self, filename: str, save_output: bool = True, save_logs: bool = True) -> Dict[str, Any]:
        """Process discussion from a file"""
        LoggingTools.log_step("FILE PROCESSING", f"Loading discussion from file: {filename}")
        
        # Load discussion content
        discussion_content = self.file_manager.load_discussion_from_file(filename)
        
        if not discussion_content:
            error_msg = f"Could not load discussion from file: {filename}"
            LoggingTools.log_error(error_msg, "File Processing")
            return {"error": error_msg}
        
        # Update discussion content and process
        self.discussion_content = discussion_content
        self.tasks = NewsGroupTasks(discussion_content)  # Reinitialize tasks with new content
        
        return self.process_discussion(save_output, save_logs)
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """Get summary of the current processing setup"""
        return {
            "content_length": len(self.discussion_content) if self.discussion_content else 0,
            "content_valid": TextProcessor.validate_discussion_content(self.discussion_content) if self.discussion_content else False,
            "environment_valid": ValidationTools.validate_environment(),
            "agents_initialized": self.agents is not None,
            "tasks_initialized": self.tasks is not None,
            "output_directory": str(self.file_manager.output_dir),
            "logs_directory": str(self.file_manager.logs_dir)
        }