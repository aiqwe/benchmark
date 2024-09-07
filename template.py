from textwrap import dedent

README_TEMPLATE = dedent(
    """
# {benchmark_name}
+ **path**: {path}  
+ **name**: {name} 
+ **url**: [{hf_url}]({hf_url})  
+ **paper**: [{paper}]({paper})  
+ **annotation**: [{annotation}]({annotation})
"""
)
