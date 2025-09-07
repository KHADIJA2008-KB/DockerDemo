import os
import warnings
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from typing import Dict, List
import time

# Suppress urllib3 SSL warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL 1.1.1+')

# Load environment variables from .env file
load_dotenv()

# Check if GOOGLE_API_KEY is available, if not prompt for it
if not os.environ.get("GOOGLE_API_KEY"):
    import getpass
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


class SpecialistAgent:
    """A specialist agent with persona, context, and memory"""
    
    def __init__(self, name: str, role: str, persona: str, expertise: str, session_id: str = None):
        self.name = name
        self.role = role
        self.persona = persona
        self.expertise = expertise
        # Use provided session_id or generate a default one
        self.session_id = session_id or f"agent_{name.lower().replace(' ', '_')}"
        
        # Store for chat histories
        self.store = {}
        
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        
        # Create specialized prompt template for this agent
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", f"""You are {self.name}, a {self.role}.

PERSONA: {self.persona}

EXPERTISE: {self.expertise}

RESPONSE GUIDELINES:
- Be CONCISE and ON-POINT - get to the key insights quickly
- Use BULLET POINTS and STRUCTURED FORMAT for clarity
- Provide ACTIONABLE ADVICE when possible
- Stay under 120 words for most responses
- Use clear, professional language
- Focus on the most critical aspects of the query

Respond as {self.name} would, drawing from your expertise in {self.role}. Be specific, practical, and stay true to your role. If you disagree with other agents, explain why from your professional perspective."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create the chain with message history
        self.chain = self.prompt | self.model
        
        # Wrap with message history
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        # Special legal knowledge enhancement for legal adviser
        if role == "Legal Adviser":
            self.legal_knowledge = self._load_legal_knowledge()
    
    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat history for the session"""
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]
    
    def respond(self, input_text: str, context: str = "", session_id: str = None) -> str:
        """Generate a response based on the agent's expertise and memory"""
        # Use the provided session_id for the chat history, fallback to agent's default if not provided
        current_session_id = session_id if session_id is not None else self.session_id
        
        # Add context to the input if provided
        full_input = f"{context}\n\n{input_text}" if context else input_text
        
        # Add legal knowledge context for legal adviser
        if hasattr(self, 'legal_knowledge') and self.legal_knowledge:
            legal_context = f"\n\nLEGAL KNOWLEDGE CONTEXT:\n{self.legal_knowledge}\n"
            full_input += legal_context
        
        response = self.chain_with_history.invoke(
            {"input": full_input},
            config={"configurable": {"session_id": current_session_id}}
        )
        
        return response.content.strip()
    
    def _load_legal_knowledge(self) -> str:
        """Load comprehensive legal knowledge for the legal adviser"""
        return """
COMPREHENSIVE LEGAL KNOWLEDGE BASE:

CORPORATE LAW:
• Business entity formation (LLC, Corp, Partnership)
• Corporate governance and compliance
• Shareholder rights and responsibilities
• Board of directors obligations
• Corporate restructuring and M&A

INTELLECTUAL PROPERTY:
• Patent law and protection strategies
• Trademark registration and enforcement
• Copyright protection and fair use
• Trade secret protection
• IP licensing and agreements

EMPLOYMENT LAW:
• Employment contracts and at-will employment
• Discrimination and harassment laws
• Wage and hour compliance (FLSA)
• Family and medical leave (FMLA)
• Workplace safety (OSHA)

CONTRACT LAW:
• Contract formation and enforceability
• Breach of contract remedies
• Statute of frauds requirements
• Contract interpretation principles
• Force majeure and impossibility

REGULATORY COMPLIANCE:
• Data privacy (GDPR, CCPA, HIPAA)
• Financial regulations (SOX, Dodd-Frank)
• Environmental compliance
• Industry-specific regulations
• International trade compliance

STARTUP LEGAL STRUCTURE:
• Founder agreements and equity splits
• Vesting schedules and cliff periods
• Intellectual property assignment
• Confidentiality and non-compete agreements
• Board composition and voting rights

FUNDRAISING COMPLIANCE:
• Securities law compliance (Reg D, Reg A+)
• Accredited investor verification
• SAFE agreements and convertible notes
• Due diligence requirements
• Regulatory filings and disclosures

INTERNATIONAL BUSINESS LAW:
• Cross-border transactions
• International contract law
• Foreign investment regulations
• Dispute resolution (arbitration vs. litigation)
• Choice of law and jurisdiction

DISPUTE RESOLUTION:
• Alternative dispute resolution (ADR)
• Arbitration clauses and enforcement
• Mediation and negotiation strategies
• Litigation procedures and timelines
• Settlement agreements and releases

RECENT LEGAL DEVELOPMENTS:
• AI and technology law updates
• Cryptocurrency and blockchain regulations
• Remote work legal considerations
• ESG compliance requirements
• Cybersecurity and data breach laws
"""
    
    def get_memory_summary(self) -> str:
        """Get a summary of the agent's conversation history"""
        history = self._get_session_history(self.session_id)
        message_count = len(history.messages)
        
        if message_count == 0:
            return "No previous discussions."
        
        return f"Has participated in {message_count//2} exchanges in this brainstorming session."


class MultiAgentBrainstormer:
    """Orchestrates multiple specialist agents in a brainstorming session"""
    
    def __init__(self):
        self.agents = self._create_agents()
        self.session_history = []
        
    def _create_agents(self) -> Dict[str, SpecialistAgent]:
        """Create the specialist agents"""
        agents = {}
        
        # Generate a consistent session ID for predefined agents
        # This ID is primarily for their internal memory management when not overridden by a chat session
        default_session_id = "predefined_agents_session"
        
        # Designer Agent
        agents['designer'] = SpecialistAgent(
            name="Alex Chen",
            role="UX/UI Designer",
            persona="Creative, user-focused, detail-oriented. Always thinks about user experience first. Loves clean, intuitive designs and accessibility.",
            expertise="User experience design, interface design, user research, design systems, accessibility, visual design principles, prototyping",
            session_id=default_session_id
        )
        
        # Marketer Agent
        agents['marketer'] = SpecialistAgent(
            name="Sarah Martinez",
            role="Marketing Strategist",
            persona="Data-driven, persuasive, market-savvy. Always considers target audience, positioning, and growth potential. Thinks in terms of campaigns and metrics.",
            expertise="Market research, brand positioning, digital marketing, customer acquisition, pricing strategy, competitive analysis, growth hacking",
            session_id=default_session_id
        )
        
        # Engineer Agent
        agents['engineer'] = SpecialistAgent(
            name="David Kim",
            role="Software Engineer",
            persona="Logical, practical, security-conscious. Always considers technical feasibility, scalability, and maintainability. Prefers proven technologies.",
            expertise="Software architecture, full-stack development, database design, API development, cloud infrastructure, security, performance optimization",
            session_id=default_session_id
        )
        
        # Investor Agent
        agents['investor'] = SpecialistAgent(
            name="Rachel Goldman",
            role="Venture Capitalist",
            persona="Analytical, risk-aware, ROI-focused. Always evaluates market size, business model, and growth potential. Thinks about exit strategies and scalability.",
            expertise="Business model evaluation, market analysis, financial projections, risk assessment, startup valuation, investment strategy, exit planning",
            session_id=default_session_id
        )
        
        # Legal Adviser Agent
        agents['legal'] = SpecialistAgent(
            name="Elena Rodriguez",
            role="Legal Adviser",
            persona="Precise, thorough, compliance-focused. Always considers legal implications, regulatory requirements, and risk mitigation. Thinks in terms of legal frameworks and precedents.",
            expertise="Corporate law, intellectual property, employment law, contract law, regulatory compliance, data privacy (GDPR, CCPA), startup legal structure, fundraising compliance, international business law, dispute resolution",
            session_id=default_session_id
        )
        
        return agents
    
    def brainstorm_idea(self, idea: str, rounds: int = 3) -> Dict:
        """Conduct a multi-round brainstorming session"""
        print(f"\n🧠 MULTI-AGENT BRAINSTORMING SESSION")
        print(f"💡 Idea: {idea}")
        print("=" * 60)
        
        context = f"We are brainstorming about: {idea}"
        current_discussion = idea
        
        session_results = {
            "original_idea": idea,
            "rounds": [],
            "final_plan": "",
            "consensus_reached": False
        }
        
        for round_num in range(1, rounds + 1):
            print(f"\n🔄 ROUND {round_num}")
            print("-" * 30)
            
            round_responses = {}
            
            # Each agent responds to the current discussion
            for agent_key, agent in self.agents.items():
                print(f"\n👤 {agent.name} ({agent.role}):")
                
                response = agent.respond(current_discussion, context, session_id=f"brainstorm_{idea.lower().replace(' ', '_')}")
                round_responses[agent_key] = {
                    "agent": agent.name,
                    "role": agent.role,
                    "response": response
                }
                
                print(f"   {response}")
                time.sleep(1)  # Small delay for readability
            
            session_results["rounds"].append(round_responses)
            
            # Update context with all responses for next round
            context += f"\n\nRound {round_num} responses:\n"
            for agent_key, resp in round_responses.items():
                context += f"- {resp['agent']}: {resp['response']}\n"
            
            # Prepare discussion for next round
            if round_num < rounds:
                current_discussion = self._synthesize_round(round_responses, session_id=f"brainstorm_{idea.lower().replace(' ', '_')}")
                print(f"\n📝 Synthesis for next round: {current_discussion}")
        
        # Generate final consensus plan
        final_plan = self._generate_final_plan(session_results, session_id=f"brainstorm_{idea.lower().replace(' ', '_')}")
        session_results["final_plan"] = final_plan
        session_results["consensus_reached"] = True
        
        return session_results
    
    def _synthesize_round(self, responses: Dict, session_id: str) -> str:
        """Synthesize the round responses into key points for the next round"""
        synthesis_prompt = "Based on these expert opinions, identify the key points of agreement, disagreement, and areas that need further exploration:\n\n"
        
        for resp in responses.values():
            synthesis_prompt += f"- {resp['role']}: {resp['response']}\n"
        
        synthesis_prompt += "\nSummarize the main themes and questions that should be addressed in the next round:"
        
        # Use one of the agents to synthesize (we'll use the designer as they're good at synthesis)
        synthesizer = self.agents['designer']
        synthesis = synthesizer.respond(synthesis_prompt, "Synthesis and facilitation", session_id=session_id)
        
        return synthesis
    
    def _generate_final_plan(self, session_results: Dict, session_id: str) -> str:
        """Generate a comprehensive final plan based on all rounds"""
        print(f"\n📋 GENERATING FINAL PLAN...")
        print("-" * 30)
        
        # Compile all insights
        all_insights = "Expert insights from brainstorming session:\n\n"
        
        for round_num, round_data in enumerate(session_results["rounds"], 1):
            all_insights += f"Round {round_num}:\n"
            for resp in round_data.values():
                all_insights += f"- {resp['role']}: {resp['response']}\n"
            all_insights += "\n"
        
        # Generate final plan
        final_prompt = f"""Based on this comprehensive brainstorming session about "{session_results['original_idea']}", create a detailed final plan that synthesizes all expert perspectives.

{all_insights}

Create a structured final plan that includes:
1. Executive Summary
2. Key Features/Components
3. Target Market & Positioning
4. Technical Implementation Strategy
5. Marketing & Go-to-Market Strategy
6. Financial Considerations
7. Risk Assessment & Mitigation
8. Next Steps & Timeline

Make it comprehensive but concise, incorporating insights from all specialists."""
        
        # Use the investor agent for final synthesis (they're good at comprehensive planning)
        final_planner = self.agents['investor']
        final_plan = final_planner.respond(final_prompt, "Final plan synthesis", session_id=session_id)
        
        return final_plan
    
    def interactive_session(self):
        """Run an interactive brainstorming session"""
        print("\n🚀 DYNAMIC MULTI-AGENT BRAINSTORMER")
        print("=" * 50)
        print("Meet your expert panel:")
        
        for agent in self.agents.values():
            print(f"👤 {agent.name} - {agent.role}")
            print(f"   {agent.persona}")
            print()
        
        while True:
            print("\nOptions:")
            print("1. Start new brainstorming session")
            print("2. Ask a specific question to all agents")
            print("3. Talk to a specific agent")
            print("4. Exit")
            
            choice = input("\nChoose an option (1-4): ").strip()
            
            if choice == '1':
                idea = input("\n💡 Enter your idea to brainstorm: ").strip()
                if idea:
                    rounds = int(input("How many rounds of discussion? (default 3): ") or "3")
                    # Pass a unique session_id for brainstorming sessions
                    results = self.brainstorm_idea(idea, rounds)
                    
                    print(f"\n🎯 FINAL PLAN:")
                    print("=" * 50)
                    print(results["final_plan"])
                    
            elif choice == '2':
                question = input("\n❓ Ask your question to all agents: ").strip()
                if question:
                    print(f"\n📢 Question: {question}")
                    print("-" * 40)
                    
                    # Use a consistent session ID for general questions to all agents
                    general_session_id = "general_questions_session"
                    for agent in self.agents.values():
                        print(f"\n👤 {agent.name} ({agent.role}):")
                        response = agent.respond(question, session_id=general_session_id)
                        print(f"   {response}")
                        
            elif choice == '3':
                print("\nAvailable agents:")
                for i, (key, agent) in enumerate(self.agents.items(), 1):
                    print(f"{i}. {agent.name} ({agent.role})")
                
                try:
                    agent_choice = int(input("\nChoose agent (number): ")) - 1
                    agent_keys = list(self.agents.keys())
                    
                    if 0 <= agent_choice < len(agent_keys):
                        selected_agent = self.agents[agent_keys[agent_choice]]
                        question = input(f"\n💬 Ask {selected_agent.name}: ").strip()
                        
                        if question:
                            # Use a specific session ID for direct interaction with an agent
                            direct_chat_session_id = f"direct_chat_{selected_agent.name.lower().replace(' ', '_')}"
                            response = selected_agent.respond(question, session_id=direct_chat_session_id)
                            print(f"\n{selected_agent.name}: {response}")
                    else:
                        print("Invalid choice!")
                        
                except ValueError:
                    print("Please enter a valid number!")
                    
            elif choice == '4':
                print("\n👋 Thanks for using the Multi-Agent Brainstormer!")
                break
                
            else:
                print("Invalid choice! Please try again.")


def main():
    """Main function to run the Multi-Agent Brainstormer"""
    brainstormer = MultiAgentBrainstormer()
    brainstormer.interactive_session()


if __name__ == "__main__":
    main()