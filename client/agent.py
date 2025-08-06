import asyncio
from mcp_agent.core.fastagent import FastAgent
import csv

prompt_file = "ENTER/FILE/PATH"
output_file = "ENTER/FILE/PATH"

# Create the application
fast = FastAgent("fast-agent example")


# Define the agent
@fast.agent(instruction="You are a helpful AI Agent")
@fast.agent(
    "Tool User",
    "Call the tools you think are appropriate according to the instructions and return the results.",
    servers=[]
)

async def main():

    async with fast.run() as agent:
        with open(prompt_file, mode='r', encoding='utf-8') as csv_file, \
            open(output_file, mode='w', encoding='utf-8', newline='') as out_file:
            
            csv_reader = csv.DictReader(csv_file)
            fieldnames = csv_reader.fieldnames + ['result']
            csv_writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            
            for row in csv_reader:
                result = await agent.send(row['question'])
                row['result'] = result
                csv_writer.writerow(row)

if __name__ == "__main__":
    asyncio.run(main())
