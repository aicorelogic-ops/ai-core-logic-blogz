import os
import google.generativeai as genai
import traceback
from .settings import GOOGLE_API_KEY

if not GOOGLE_API_KEY:
    print("Warning: GOOGLE_API_KEY is not set.")

# Configure Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    model = None

class NewsProcessor:
    def summarize(self, article):
        """
        Takes an article dict and returns a DICT with:
        - 'blog_html': Full HTML analysis for the website.
        - 'facebook_msg': Short teaser for social media.
        """
        if not model:
            print("Skipping summarization: Gemini model not initialized.")
            return None

        prompt = f"""
        You are a Direct Response Copywriter for 'AI Core Logic' - writing in the style of Sabri Suby.
        
        Input:
        Title: {article['title']}
        Summary: {article['summary']}
        
        CORE PRINCIPLES:
        - HIGH-READABILITY: Structure for scanners first. Most important info at the TOP.
        - HIGH-AROUSAL EMOTION: Evoke awe, anxiety, or anger to drive virality.
        - NO FLUFF: One idea per sentence. 6th grade reading level.
        - MOBILE-FIRST: Paragraphs must be 1-3 sentences max.
        
        Task: Create TWO outputs in a strictly formatted way.
        
        Output 1: A BLOG POST (HTML Format)
        **STRUCTURE SPECS:**
        
        1. **PATTERN INTERRUPT HOOK**: Start with a shocking statement or number.
        
        2. **PPT INTRO (Preview, Proof, Transition)**:
           - PREVIEW: What is this post about?
           - PROOF: Why should they listen? (Expertise/Data)
           - TRANSITION: Move them into the body content.
           
        3. **INVERTED PYRAMID**: Put the "Who, What, When, Where, Why" in the first 2 paragraphs.
        
        4. **LAYER-CAKE SCANNING**:
           - Use BOLD and DESCRIPTIVE H2/H3 headers.
           - Use BULLET POINTS (<ul><li>) for key data.
           - NO generic headers like "Introduction" or "Conclusion".
           
        5. **SABRI SUBY STYLE**: 80% agitation of pain/desire, 20% solution.
        
        6. **TAC CONCLUSION (Transition, Ask, Call to Action)**:
           - TRANSITION: Signal the end of the content.
           - ASK: Ask a specific question to encourage comments/shares.
           - CALL TO ACTION: Tell them exactly what to do next.
        
        **CONTENT RULES**:
        - Use H2 for major segments and H3 for sub-points.
        - Keep paragraphs 1-3 sentences for mobile readability.
        - Take a strong stance. Be opinionated.
        
        Output 2: A FACEBOOK POST (Plain Text, SHORT & PUNCHY)
        **KEEP IT SHORT - Long posts are boring, nobody reads them**
        - Lead with the hook emoji + shocking statement
        - 2-3 punchy sentences of pain (short!)
        - 1 sentence with intrigue/benefit
        - Link + strong CTA
        - Include emojis for pattern interrupt (🚨, 🔥, ⚡, 💡)
        - End with: "Full story: [LINK]"
        - CRITICAL: Include 5-7 relevant hashtags at the very end
        
        Example structure:
        🚨 [Shocking hook in 10 words max]
        
        [Pain sentence 1]. [Pain sentence 2]. 
        
        [Intrigue: "Here's what we found..." or "The solution: ..."]
        
        Full story: [LINK]
        
        #Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5
        
        CRITICAL RETURN FORMAT:
        - DO NOT include labels like "Output 1:" or "Output 2:" in your response
        - DO NOT include any markdown formatting indicators like **text** in the Facebook post
        - Separate the two outputs ONLY with the delimiter "|||||"
        - First part = HTML blog content (can use HTML tags)
        - Second part = Plain text Facebook post (NO labels, NO markdown, NO formatting indicators)
        - The Facebook post should start IMMEDIATELY with the content, not with any header
        """

        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            # Split the response
            if "|||||" in text:
                parts = text.split("|||||")
                blog_html = parts[0].strip()
                facebook_msg = parts[1].strip()
                
                # Clean up Facebook message - remove any instruction labels or formatting indicators
                # Remove common AI output labels
                facebook_msg = facebook_msg.replace('**OUTPUT 2: A FACEBOOK POST (Plain Text, LONG-FORM 200+ words)**', '')
                facebook_msg = facebook_msg.replace('OUTPUT 2: A FACEBOOK POST (Plain Text, LONG-FORM 200+ words)', '')
                facebook_msg = facebook_msg.replace('**OUTPUT 2:**', '')
                facebook_msg = facebook_msg.replace('OUTPUT 2:', '')
                facebook_msg = facebook_msg.replace('**Facebook Post:**', '')
                facebook_msg = facebook_msg.replace('Facebook Post:', '')
                
                # Clean up any remaining markdown bold markers in plain text
                import re
                # Only remove ** markers if they're wrapping instruction-like text at the start
                if facebook_msg.startswith('**'):
                    facebook_msg = re.sub(r'^\*\*[^*]+\*\*\s*', '', facebook_msg)
                
                facebook_msg = facebook_msg.strip()
                
                return {
                    "blog_html": blog_html,
                    "facebook_msg": facebook_msg
                }
            else:
                # Fallback if AI forgets delimiter
                return {
                    "blog_html": f"<p>{text}</p>",
                    "facebook_msg": "New AI Update! Check our blog. [LINK]"
                }

        except Exception as e:
            print(f"Error generating summary with Gemini: {e}")
            with open("error_log.txt", "w", encoding="utf-8") as panic_log:
                traceback.print_exc(file=panic_log)
            return None

if __name__ == "__main__":
    # Test run
    processor = NewsProcessor()
    sample_article = {
        "title": "New AI Tool Automates Invoice Processing",
        "summary": "A new startup has released a tool that reads PDF invoices with 99% accuracy.",
        "link": "http://example.com"
    }
    result = processor.summarize(sample_article)
    print("BLOG:", result['blog_html'][:50] if result else "None")
    print("FB:", result['facebook_msg'] if result else "None")
