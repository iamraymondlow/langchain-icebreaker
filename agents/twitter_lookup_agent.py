from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from tools.tools import get_profile_url

from langchain.agents import initialize_agent, Tool, AgentType


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    template = """given the name {name_of_person} I want you to get me a link to their twitter profile page and extract
                    their username. your answer should only contain the person's username"""
    tools_for_agent = [
        Tool(
            name="Crawl Google for twitter profile page",
            func=get_profile_url,
            description="useful for when you need to get the twitter page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return twitter_username
