import streamlit as st
import openai
import json
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="AI DM Assistant Pro",
    page_icon="✉",
    layout="wide"
)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_personalized_message(prospect_info, goal, tone, platform):
    """Generate a personalized message using OpenAI"""
    client = get_openai_client()
    
    prompt = f"""
    Create a highly personalized direct message based on this information:
    
    Prospect Information: {prospect_info}
    Goal: {goal}
    Tone: {tone}
    Platform: {platform}
    
    Requirements:
    - 50-120 words maximum
    - Reference specific details from the prospect's profile
    - Professional yet {tone.lower()} tone
    - Clear but soft call-to-action
    - Avoid being salesy or pushy
    - Include a genuine compliment or observation
    
    Return only the message text, no additional formatting.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at crafting personalized, engaging professional messages."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating message: {str(e)}"

def generate_multiple_drafts(prospect_info, goal, tone, platform):
    """Generate 3 different message drafts"""
    drafts = []
    for i in range(3):
        message = generate_personalized_message(prospect_info, goal, tone, platform)
        drafts.append({
            "draft_number": i + 1,
            "message": message,
            "word_count": len(message.split())
        })
    return drafts

# Main App Interface
def main():
    # Header
    st.title("✉ AI DM Assistant Pro")
    st.markdown("*Generate personalized messages that get responses*")
    
    # Sidebar for upgrade promotion
    with st.sidebar:
        st.markdown("### 🚀 Upgrade to Pro!")
        st.markdown("""
        *Current: Free Version*
        - 5 messages per day
        - Basic personalization
        
        *Pro Version ($29/month):*
        - ✅ Unlimited messages
        - ✅ Advanced AI analysis
        - ✅ Performance tracking
        - ✅ A/B testing
        - ✅ Priority support
        
        [*Upgrade Now*](mailto:your-email@gmail.com?subject=Pro%20Upgrade%20Request)
        """)
        
        st.markdown("---")
        st.info("💡 *Tip:* Always review and personalize AI drafts before sending!")
    
    # Main input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Prospect Information")
        prospect_info = st.text_area(
            "Paste information about your prospect:",
            height=120,
            placeholder="""Example:
Sarah Johnson, VP Marketing at TechStartup Inc.
- Recently posted about AI in marketing on LinkedIn
- Stanford MBA graduate
- Interested in sustainable business practices
- Just launched new product campaign for eco-friendly software
- Active in Women in Tech communities
- Company raised $5M Series A last month"""
        )
        
        goal = st.text_input(
            "🎯 Your Goal:",
            placeholder="e.g., Schedule a 15-minute demo call, Explore partnership opportunities"
        )
    
    with col2:
        st.subheader("⚙ Settings")
        tone = st.selectbox(
            "Tone:",
            ["Professional", "Friendly", "Enthusiastic", "Direct", "Casual"]
        )
        
        platform = st.selectbox(
            "Platform:",
            ["LinkedIn", "Email", "Twitter DM", "Instagram", "General"]
        )
        
        word_limit = st.slider("Word Limit:", 30, 150, 100)
    
    # Generate button
    if st.button("🚀 Generate Personalized Messages", type="primary"):
        if prospect_info and goal:
            with st.spinner("🤖 AI is crafting your personalized messages..."):
                drafts = generate_multiple_drafts(prospect_info, goal, tone, platform)
                
                st.success("✅ Generated 3 personalized message drafts!")
                
                # Display drafts
                st.subheader("📝 Your Message Drafts")
                
                for draft in drafts:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        
                        with col1:
                            st.markdown(f"*Draft {draft['draft_number']}:*")
                            message_text = st.text_area(
                                f"Message {draft['draft_number']}",
                                value=draft['message'],
                                height=100,
                                key=f"draft_{draft['draft_number']}",
                                label_visibility="collapsed"
                            )
                        
                        with col2:
                            word_count = draft['word_count']
                            if word_count <= word_limit:
                                st.success(f"✅ {word_count} words")
                            else:
                                st.warning(f"⚠ {word_count} words")
                            
                            if st.button(f"📋 Copy", key=f"copy_{draft['draft_number']}"):
                                st.code(message_text)
                        
                        st.markdown("---")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📊 Analyze Performance"):
                        st.info("📈 Performance analytics available in Pro version")
                
                with col2:
                    if st.button("🔄 Generate New Variants"):
                        st.rerun()
                
                with col3:
                    if st.button("💾 Save Session"):
                        st.success("💾 Session saving available in Pro version")
        
        else:
            st.warning("⚠ Please provide both prospect information and your goal.")
    
    # Footer
    st.markdown("---")
    st.markdown("💡 Pro Tip:** Personalize these drafts further before sending for best results!")
    
    # Usage stats (placeholder)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Messages Generated Today", "3", "3")
    with col2:
        st.metric("Avg Response Rate", "23%", "5%")
    with col3:
        st.metric("Time Saved", "45 min", "15 min")

if _name_ == "_main_":
    main()
