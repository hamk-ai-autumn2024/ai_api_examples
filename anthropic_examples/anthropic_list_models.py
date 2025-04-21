import anthropic

# Asuming you have set the ANTHROPIC_API_KEY environment variable
client = anthropic.Anthropic()
models = client.models.list(limit=30)
print("Models:")
for model in models:
    print(model)
# print(models)