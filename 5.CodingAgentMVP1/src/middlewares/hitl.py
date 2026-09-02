# Prepare a sinmple function that can help us to inject HITL to any agent in langchain


from langchain.agents .middleware import HumanInTheLoopMiddleware

def build_hitl_middleware()-> HumanInTheLoopMiddleware:
    return HumanInTheLoopMiddleware(
       interrupt_on={
         "read_files": False, # no hitl for read files
         "list_files": False, # no hitl for list files
         "write_files": {
            "file_path": ["approve", 'edit', "reject"],
            "description":"Write or overwrite a file on disk"
         },
         "edit_file":{
            "file_path": ["approve", 'edit', "reject"],
            "description":"Edit an existing file on disk"
         }
       },
       default_action="Coding agent needs your approval to move ahead"
    ) 