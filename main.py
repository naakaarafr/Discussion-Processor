#!/usr/bin/env python3
"""
NewsGroup Discussion Processor - Main Entry Point

This script demonstrates how to use the NewsGroup crew system to:
1. Filter spam content
2. Transform discussions into movie-style dialogue
3. Score the quality of the transformation
4. Save results to files

Usage:
    python main.py
    python main.py --file discussion.txt
    python main.py --no-save
"""

import os
import sys
import argparse
from pathlib import Path
from crew import NewsGroupCrew
from tools import LoggingTools, ValidationTools

# Sample discussion for demo purposes
SAMPLE_DISCUSSION = """
John: I've been thinking about the new climate policy proposals. They seem pretty comprehensive.

Sarah: Really? I read through them yesterday and I'm not convinced they go far enough. The carbon tax rates are still too low compared to what scientists recommend.

Mike: But Sarah, you have to consider the economic impact. If we raise taxes too high too fast, we could hurt small businesses and working families.

Sarah: Mike, that's exactly the kind of short-term thinking that got us into this mess. We need bold action now, not incremental changes that won't make a difference.

John: I see both sides here. Maybe there's a middle ground? What if we implemented the tax gradually over 5 years with support programs for affected businesses?

Mike: That's more reasonable, John. I could support something like that. Sarah, what do you think?

Sarah: I suppose it's better than nothing, but I still think we're not moving fast enough. Climate change won't wait for our economic convenience.

John: Fair point, Sarah. But political reality matters too. If we push too hard and lose the next election, we might get nothing at all.

Mike: Exactly. Sometimes incremental progress is better than no progress.

Sarah: I understand that, but I worry we're compromising away our children's future. Someone has to advocate for bold action.
"""

def setup_environment():
    """Setup environment variables if not already set"""
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  GOOGLE_API_KEY not found in environment")
        print("💡 You can:")
        print("   1. Set it as an environment variable")
        print("   2. Create a .env file with GOOGLE_API_KEY=your_key_here")
        print("   3. Set it temporarily for this session")
        
        # Try to load from .env file
        env_file = Path(".env")
        if env_file.exists():
            print("📁 Found .env file, loading...")
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            os.environ[key] = value
                print("✅ Environment variables loaded from .env")
            except Exception as e:
                print(f"❌ Error loading .env file: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Process newsgroup discussions into dialogue")
    parser.add_argument("--file", "-f", help="Input file containing discussion")
    parser.add_argument("--no-save", action="store_true", help="Don't save output files")
    parser.add_argument("--no-logs", action="store_true", help="Don't save log files")
    parser.add_argument("--demo", action="store_true", help="Run with sample discussion")
    
    args = parser.parse_args()
    
    print("🚀 NewsGroup Discussion Processor")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Determine input source
    discussion_content = None
    source = "unknown"
    
    if args.file:
        source = f"file: {args.file}"
        print(f"📁 Loading discussion from file: {args.file}")
        # We'll let the crew handle file loading
    elif args.demo or len(sys.argv) == 1:  # No arguments provided, use demo
        source = "sample discussion"
        discussion_content = SAMPLE_DISCUSSION
        print("📝 Using sample discussion for demonstration")
    else:
        print("❌ No input provided. Use --file to specify a file or --demo for sample content")
        return 1
    
    try:
        # Initialize crew
        if args.file:
            # Create crew with dummy content first, then process from file
            crew = NewsGroupCrew("dummy content")
            print(f"🔧 Processing discussion from {source}")
            result = crew.process_from_file(
                args.file, 
                save_output=not args.no_save,
                save_logs=not args.no_logs
            )
        else:
            crew = NewsGroupCrew(discussion_content)
            print(f"🔧 Processing discussion from {source}")
            result = crew.process_discussion(
                save_output=not args.no_save,
                save_logs=not args.no_logs
            )
        
        # Display results
        print("\n" + "=" * 60)
        print("📊 PROCESSING RESULTS")
        print("=" * 60)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            return 1
        
        elif result["status"] == "filtered":
            print(f"🚫 Content Filtered: {result['message']}")
            return 0
        
        elif result["status"] == "success":
            print(f"✅ Status: {result['message']}")
            print(f"📏 Original length: {result['stats']['original_length']} characters")
            print(f"📏 Processed length: {result['stats']['processed_length']} characters")
            print(f"💾 Files saved: {result['stats']['files_saved']}")
            
            print(f"\n🎭 GENERATED DIALOGUE (Score: {result['score']}/10)")
            print("-" * 50)
            
            # Display dialogue with truncation for long content
            dialogue = result['dialogue']
            if len(dialogue) > 1000:
                print(dialogue[:1000])
                print(f"\n... [truncated - full dialogue saved to file] ...")
                print(f"\n📁 Check output/dialogue_output.txt for complete dialogue")
            else:
                print(dialogue)
            
            print(f"\n🏆 Quality Score: {result['score']}/10")
            
            if not args.no_save:
                print(f"\n📂 Output files saved to: output/")
                print("   • dialogue_output.txt - The generated dialogue")
                print("   • dialogue_score.txt - Score and details")
            
            if not args.no_logs:
                print("   • logs/ - Processing logs")
        
        print("\n✨ Processing complete!")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Processing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        print("💡 Check your environment setup and try again")
        return 1

def create_sample_file():
    """Helper function to create a sample discussion file"""
    sample_file = Path("sample_discussion.txt")
    if not sample_file.exists():
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_DISCUSSION)
        print(f"📄 Created sample file: {sample_file}")

if __name__ == "__main__":
    # Create sample file for demonstration
    create_sample_file()
    
    # Run main function
    exit_code = main()
    sys.exit(exit_code)