import anthropic

# Asuming you have set the ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()
models = client.models.list(limit=30, model="claude-sonnet-4-20250514")
print("Models:")
for model in models:
    print(model)
# print(models)