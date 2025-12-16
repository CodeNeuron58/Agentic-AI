# LangGraph Sequential Workflow Demonstration

This repository contains example notebooks that demonstrate how to build **sequential workflows using LangGraph**.  
The focus of these examples is to explain **core LangGraph concepts** such as `StateGraph`, typed state management, node execution, and LLM integration.

---

## Core Concepts

### StateGraph

`StateGraph` is the central abstraction used to define a workflow in LangGraph.

- Represents a **directed graph of nodes**
- Each node is a Python function
- Operates on a **shared state object**
- Executes nodes in the order defined by graph edges

Example execution pattern:

```
START → Node 1 → Node 2 → ... → END
```

### START and END Nodes

Special markers define the workflow's entry and termination points:

- `START` – entry point
- `END` – termination point

Edges explicitly define execution flow, ensuring **deterministic order**.

### Typed State with TypedDict

Workflows define their state using `TypedDict` to:

- Clearly specify the data structure
- Make node inputs/outputs explicit
- Improve readability and maintainability

Example:

```python
class WorkflowState(TypedDict):
    input_value: str
    output_value: str
```

Nodes:

- Receive the full state
- Read required fields
- Update specific fields
- Return the updated state

### Nodes as Pure Functions

Nodes are Python functions that:

- Accept the current state as input
- Perform a single logical operation
- Modify or extend the state
- Return the updated state

This design ensures modularity, extensibility, and separation of responsibilities.

---

## Example Workflows

### BMI Calculation Workflow

A **non-LLM sequential workflow** demonstrating:

- State initialization with numeric values
- Sequential computation across nodes
- State mutation across steps

Steps:

1. Calculate BMI using height and weight.
2. Assign a BMI category based on the calculated value.

### Blog Generation Workflow (LLM-based)

A **multi-step LLM workflow** using Cohere, demonstrating:

- LLM usage inside LangGraph nodes
- Passing intermediate LLM outputs through state
- Sequential dependency between LLM calls

Steps:

1. Generate a blog outline from a title.
2. Generate full blog content using the outline.

### LLM Question Answering Workflow

A **minimal LLM-powered sequential workflow** demonstrating:

- Single-node workflow
- LLM invocation inside a node
- Simple question → answer state transformation

---

## Workflow Compilation and Execution

Define nodes and edges, then compile the graph:

```python
workflow = graph.compile()
```

Invoke the compiled workflow with an initial state:

```python
result = workflow.invoke(initial_state)
```

LangGraph automatically:

- Passes state between nodes
- Executes nodes in the defined order
- Returns the final state at `END`

---

## Graph Visualization

Some examples include Mermaid diagrams for:

- Understanding execution flow
- Debugging workflows
- Visual explanations

---

## Summary

These examples demonstrate:

- Stateful workflow management with LangGraph
- Explicit modeling of sequential execution
- Clarity of state transitions using TypedDict
- Structured LLM workflows

