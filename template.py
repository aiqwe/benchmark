from textwrap import dedent

README_TEMPLATE = dedent("""
# {benchmark_name}
+ **source**: {source}
+ **hf_path**: {hf_path}
+ **hf_url**: {hf_url}
+ **url**: {url}
+ **hf_name**: {hf_name} 
+ **hf_url**: [{hf_url}]({hf_url})  
+ **paper**: [{paper}]({paper})  
+ **annotation**: [{annotation}]({annotation})
""")
