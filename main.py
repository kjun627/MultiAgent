import agent.interface as agent

if __name__ == "__main__":
    # agent = agent.Agent252DBase(name="Agent252D", role="a helpful assistant")
    # agent.run()
    
    agent_with_memory = agent.Agent252DWithMemory(name="Agent252DWithMemory", role="a helpful assistant")
    agent_with_memory.run()