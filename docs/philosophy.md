This document captures the development philosophy you should follow throughout all the stages of work.

## Generic
- This codebase follows Daoism. The code should flow like water, non-doing, not forced, natural code.
- The code should remain flexible. Don't repeat, don't create many tests for the same capability, keep things lean, to easily adjust and change
- Development is partitioned by subpackage. Don't spread development throughout multiple subpackages. Start development on one module, finish, run the tests, then move to the next. Don't parallelize.
- Always write production code. Code that you can happily publish online or let a teammate to review. Don't leave unnecessary comments.
- Always leave the codebase in better shape than before you touched it. If you see small syntax issues, go ahead and solve. If you see bigger problems, create tasks in backlog.
- Never try to solve vague problem directly. Instead, ask for clarifications or more information, write a high level plan and review, then break down into subproblems, create a tracker document with a checklist, and step by step solve while maintaining the tracker document.
- Use """ for multiline strings

## Project Management
- Employ iterative development: Plan phases, deliver incrementally, and adapt based on feedback or changing requirements.
- Define clear scope: Establish boundaries early (e.g., Charter & Scope in a project plan) and manage scope creep proactively.
- Practice risk management: Identify potential risks, assess their impact, and define mitigation strategies upfront (e.g., Risks & Mitigation in a project plan).
- Maintain project visibility: Use planning documents and task trackers (`tasks.md`) to ensure alignment and track progress.

## Task Management
- Follow Kanban principles: Address tasks from `tasks.md` sequentially, one at a time. Focus on completing a task before starting the next.
- When the user asks to create a task, add it to the tasks.md file.
- Update task status in `tasks.md` upon completion or if blocked.
- Ensure code changes directly address the acceptance criteria of the current task.
- For complex tasks requiring planning or design, create draft documents (e.g., markdown files) within `docs/tasks/{task_id}/` for review or clarification before implementation.
- It's your responsibility to update the task statuses.
- Work only on one task at a time.
- For requests without existing tasks, always create a task and track it there.

## Design documents
- By "design document" we refer to a document that clearly calls out the problem we are trying to solve, defines the terms, list assumptions, provides historic/tech context, then from first principles builds up the possible solutions using different approaches/perspectives/models/philosophies. Then provides a recommended path forward.
- Then we go through reviews of the document, you accept feedback, provide more information if needed, adjust the document as needed, while trying to foresee possible issues and risks.
- We write design documents for non-trivial tasks.

## Coding
- Use Clean Code principles. Approach to this like craftsmanship.

## Testing
- Create unit tests for each package, verifying the public methods
- Use clear naming pattern for the test names: `test_methodName_expectedBehaviour_inWhichSituation` - even if the method_name uses snake case, convert it to camelCase like methodName
- Test-driven development - write the unit test for the capability you want, then implement
- Remember, code needs to be written testable, not all code is testable.
- For testing using pytest, use fixtures if needed
- In the tests write dummy data, never put real paths/names/data
- When checking strings, verify the whole string at once, don't just check pieces. Use multiline text blocks if needed. So write only one assert if you anyway want to verify the whole string.
- Use AAA (Arrange, Act, Assert)
- Create a class per test file, add the unit tests inside the class
- Prefer automated tests over manual tests
- Test files should mimic the source code directory structure. A/B/C.py will be tested in tests/A/B/test_C.py
- Write minimum number of tests, while making sure all features/capabilities are covered. Use black box testing approach, testing the contract through the public methods. Test internals only in rare cases when it's an important logic hard to test from outside.

## Implementation

- Create subpackages in python
- Create interface (ABC) in __init__.py, don't import the implementation here
- Use dependency injection from the `main` function when instantiating the implementations
- Have separate files for the implementation classes
- Nest packages logically
- Check if the interface needs to be updated, does it pass all the necessary information?
- Have detailed logging (through `logger = logging.getLogger(__name__)`) with debug, concise with info
- In case you are lacking information about another class in a different subpackage, that means the interface is not good enough defined. Update the interface, maybe add return type, documentation, then ask the user to work with the team to make sure the implementation matches that interface. You can't have access to the implementation from a different subpackage.
- You find the simplest solutions for even difficult and complex problems. This might include updating existing pieces, removing some, or adding new ones.
- Whenever adding TODOs, always include a reference to a task where the TODO will be cleaned up/resolved.
- Write lean code, don't create backup solutions/codepaths if not necessary. Find the right way and see if that can be the only way, support complexity only if needed.
