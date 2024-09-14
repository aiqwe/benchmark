from textwrap import dedent

README_TEMPLATE = dedent("""
# {benchmark_name}
+ **source**: {source}
+ **hf_path**: {hf_path}
+ **hf_name**: {hf_name} 
+ **url**: [{url}]({url})  
+ **paper**: [{paper}]({paper})  
+ **annotation**: [{annotation}]({annotation})
""")
