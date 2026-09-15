from langgraph.checkpoint.memory import IMemorySaver


def make_checkpointer()->IMemorySaver:
    return IMemorySaver()

def thread_config(thread_id:str)->dict:
    return{
        "configurable":{
            "thread_id":thread_id
        }
    }
