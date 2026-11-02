# {{package_name}}

An experimental general-purpose CrewAI Agent with three local example tools and two example skills.
The example describes a fictional service and does not access real accounts or external systems.
Standalone agent project formats and CLI support may change. Use matching preview CLI and SDK builds that include this feature.

Create this Python layout with `crewai create agent {{package_name}} --format python`.
The default command creates a YAML definition instead.
The Agent defaults to `openai/gpt-6.1-sol` through the Responses API; set `MODEL` in `.env` to choose another OpenAI model.

```text
{{package_name}}/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
└── src/{{package_name}}/
    ├── __init__.py
    ├── agent.py
    ├── tools/
    │   ├── __init__.py
    │   ├── support_hours.py
    │   ├── lookup_plan.py
    │   └── support_checklist.py
    └── skills/
        ├── support-triage/SKILL.md
        └── response-style/SKILL.md
```

## Run the reference Agent

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`, then run:

```sh
crewai install
crewai run --inputs '{"messages":"Use support_hours to tell me when support is available."}'
crewai run --inputs '{"messages":"I use the Pro plan and cannot sign in. Use the support-triage and response-style skills to explain what I should try and when support is available. Write a short customer reply."}'
crewai deploy validate
```

`crewai install` creates `uv.lock`. Commit it before deploying; keep `.env` local.

## Customize the Agent

The default identity is general-purpose. Edit its role, goal, and backstory to specialize it, and add, replace, or remove tools and skills to match the task. The included support examples apply only when relevant.

## Example tools and skills

| Tool | Input | Example result |
| --- | --- | --- |
| `support_hours` | None | Monday to Friday, 09:00-17:00 UTC |
| `lookup_plan` | `plan`: `starter` or `pro` | Seat allowance and support channel |
| `support_checklist` | `topic`: `sign-in` or `billing` | Troubleshooting steps |

The plan and checklist tools demonstrate typed Pydantic argument schemas and JSON results.
Unknown values return the available choices. Replace these example facts with your own application logic.

| Skill | When to use it |
| --- | --- |
| `support-triage` | Multi-step questions requiring tool results and an escalation path |
| `response-style` | Turning verified facts into a concise customer reply |

Skills begin as a metadata catalog. The Agent can call its `load_skill` tool to read a relevant skill's full instructions.

Edit `src/{{package_name}}/agent.py` to configure the exported `agent`.
Import new tools from `.tools` and add their instances to `tools=[...]`.
Add `skills/<name>/SKILL.md` under the Python package with `name` and `description` frontmatter to extend the skill catalog.
The skill path is anchored to `agent.py`, so loading from another working directory works.
The tools and skills live inside the package and ship in its wheel and deployment archive.
Load only trusted projects: the Python definition and custom tools execute during loading.

The local runner and managed runtime load the same `agent = Agent(...)` definition.
`messages` accepts a string or a list of role/content messages. Each kickoff creates a fresh Agent; conversation history is not persisted automatically.
