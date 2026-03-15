# Prompt Design Framework

There's no single way to prompt AI. The key is being clear and specific to what you are trying to achieve and providing context. A good prompt follows a simple framework and contains the following components: persona, task, format, and context.

- **Persona:** The expertise you want AI to draw from.
- **Task:** What you want AI to help with.
- **Format:** How you want the results to appear.
- **Context:** Any background information AI needs to help you with this task.

## Example Prompt

Let's take a look at a prompt that includes all of the components mentioned above:

> "You are a seasoned advertising writer. Create a concise tagline that highlights the key features of a new washing machine. The washing machine's features are that it gets clothes extra clean, has 25 customizable settings, and fits in a small space. The tagline should use an active voice, and be no more than 6 words."

Do you notice how this prompt uses each component?

- **Persona:** You are a seasoned advertising writer.
- **Task:** Create a concise tagline that highlights the key features of a new washing machine.
- **Format:** The tagline should use an active voice, and be no more than 6 words.
- **Context:** The washing machine's features are that it gets clothes extra clean, has 25 customizable settings, and fits in a small space.

---

# Prompt Writing Tips and Best Practices

Follow the three C's when writing your prompts. How you approach writing your prompts dramatically impacts the result.

1. **Be concise:** Keep prompts simple and avoid overly long or complex requests in a single prompt. A prompt that is short and to the point generally requires less processing from AI.

2. **Be clear:** Be precise and avoid contradictory or ambiguous instructions. Vague prompts, like "Make this better," give AI too many possible paths and require it to make assumptions. Instead, give clearer direction with a more specific prompt, like "Revise this text to be more formal and add a call to action."

3. **Be consistent:** Use the same vocabulary for the same concepts throughout your conversation with AI. For example, if you refer to a "spreadsheet" in your initial prompt, continue to say spreadsheet throughout the rest of your conversation. Using words like "matrix" or "tab" interchangeably in the same chat might confuse AI.

---

# Always Evaluate the Output

It's important to evaluate the quality of AI output before using or sharing it. AI models can be prone to "hallucinations" — confident but incorrect responses — for several reasons:

Hallucinations can happen when there were mistakes in the original training data, or when the AI has been asked to solve a never-seen-before problem or to understand real-world knowledge and physical things. On some occasions, the model may prioritize generating a plausible-sounding answer in order to satisfy the user's prompt, effectively serving as a guess.

Another reason to evaluate AI output is because different AI models are programmed differently. Some models may be better suited to specific uses like writing code, while others might have limited outputs based on their specific training sets.

When evaluating AI output, focus on these key factors:

- **Accuracy:** Is the information correct and factually sound?
- **Bias:** Does the output favor one perspective unfairly because of its training data?
- **Relevancy:** Does it directly answer your prompt and stay on topic?
- **Consistency:** Is the tone, style, and quality the same throughout the response?

> Any AI-generated output should serve as a starting point, not a final product. If an output isn't what you need, iterate.

---

# Improve Your Results with Iterative Prompting

Using the following techniques to clarify and refine your prompts (also known as iteration) can help you get better outputs.

1. **Revisit the prompting guidelines:** If your prompt isn't giving you the results you need, try editing it by adding more detail to your persona, task, format, or context.
   
   - *Initial prompt:* Identify the latest developments in the restaurant industry.
   - *Improved prompt:* Acting as a restaurant marketing expert, create a bulleted list including the latest developments related to consumer price and quality expectations in the fast-casual restaurant industry.

2. **Break up complex tasks:** Don't ask for everything at once. Ask for smaller pieces of your task, one at a time. This helps AI process each step and lets you check in along the way.
   
   - *Step 1:* First, explain the key principles of effective decision-making.
   - *Step 2:* Now, how can I apply those principles in my weekly status meetings?

3. **Add constraints:** Add the specific requirements that AI must meet. This is an excellent way to narrow the focus of the response.
   
   - *Example:* Provide solutions that can be implemented within a week.

---

# Use References to Model Your Desired Result

References provide examples or resources that illustrate what you want AI to produce. They specify details about your desired output, such as the style, tone, and format. Depending on what AI you are using, you might be able to include text, images, audio, or even video as references. When including references in your prompts, make sure to explain how the references relate to the task.

Here's an example of a prompt that includes references:

> "Write a short social media post promoting a two-day music festival. Use the following example as a reference for tone and format: "Where mountains meet music: Indie Rocks Festival returns! Your favorite local bands + national acts. Good eats & Sleep under the stars! #Indie Rocks #SupportLocalMusic""

Effective prompting relies on using a clear framework — persona, task, format, and context — combined with an iterative process of refinement. By following the three C's and treating AI outputs as a starting point, you can consistently guide the AI to deliver accurate and high-quality results.

---

# Use New Chats for New Topics

A context window is the limit of how much information AI can retain and refer back to within a single chat. It allows AI to refer back to earlier parts of your conversation so its answers stay consistent. Because of this, you should always start a new chat when changing topics. This ensures AI only focuses on information that is relevant to your current task. If you switch to a completely new topic within the same chat, AI might use the unrelated context provided earlier, and generate an irrelevant or misguided response.

For example, if you were discussing messaging for a marketing campaign and now want to write a professional bio for your resume, start a new chat.

---

# Save Your Best Prompts in a Library

Like any skill, your prompt writing abilities will improve through experimentation and practice. As you get more experience, you can save time by noting which prompts work best and reusing them.

- **Create a personal prompt library:** When a prompt gives you a great result, name it and save it for future use. Some AI tools even have this feature built-in.

- **Don't reinvent the wheel:** Once you have a successful prompt template, use it as your base. You can experiment by tweaking certain elements of the prompt like the task, persona, format, or context to get different results without starting from scratch.
  
  *Example:*
  
  > "Help me with a [task]. Use the expertise of [persona] when completing this task. The output should be [format]. Before you help me with this task, you should know that [context]."

- **Learn from your colleagues:** Many people share successful prompts with their team. Sharing knowledge is a great way to find inspiration and learn new techniques.

---

> This article is a curated excerpt from the Google AI Professional Certificate. This certificate is your path to AI fluency, built by Google experts. You'll move beyond the basics with hands-on practice, gaining the in-demand skills and confidence to apply AI to your job from day one.

---

# The Building Blocks of More Effective Prompts

Effective prompting is built upon a foundation of four key elements: persona, task, context, and format. Building on this framework, there are two prompting techniques that are particularly effective for managing complex workflows:

- **Powerful prompt phrases:** Using specific, precise language inside a single prompt to improve the quality and depth of AI's response.
- **Prompt chaining:** Using a series of smaller, connected prompts to break down a larger, complicated request into individual questions or tasks.

---

# Guide AI with Powerful Prompt Phrases

Word choice becomes increasingly important when applying AI to complex tasks, and certain phrases can be more effective in getting you the outputs you need. Powerful prompt phrases don't just tell AI what to do. They guide how AI should get there by adding precision, setting boundaries, and forcing AI to use more complex reasoning paths.

Here are some ways to use powerful prompt phrases:

## Give AI a Process to Follow

Mandating a thought process often leads to a more accurate final answer. By directing AI models to process a request sequentially, or to follow a specific process, the AI model is likely to incorporate more constraints and details before generating an output.

Example prompt phrases may include:

- "Think step-by-step."
- "First, [action 1]. Second, [action 2]. Finally, [action 3]."

## Define the Audience and Tone

These phrases go beyond a persona and dictate the style of the output. This helps your message land correctly, whether you're drafting an email to a potential client, a report for leadership, or a social media post for your customers.

Example prompt phrases include:

- "Write this for an audience of [audience type, e.g. executives]."
- "The tone should be [tone, e.g. professional]."

## Set Hard Constraints

This can help lower the chances of the AI hallucinating (generating factually incorrect outputs) or including irrelevant information. Use this when you need content for a specific format, like a concise product description, or based on specific information, such as a sales report.

Example prompt phrases include:

- "Do not exceed 100 words."
- "Focus exclusively on [topic A] and do not mention [topic B]."
- "Use only facts, data, and information from this file."
- "Provide citations to verifiable sources for any factual claims."

## Provide Examples

Telling AI what to do is good, but giving it a reference of what good looks like is even better. This is one of the fastest ways to teach the AI your specific style. Clear examples of what you want can help get outputs that match your voice, or your brand's voice, with greater consistency. It can also help if you show it what not to do.

Example prompt phrases include:

- "Follow this pattern: [Question: ..., Answer: ...]"
- "Here is a good response: [Example 1]. Here is a bad response: [Example 2]. Give me a response that is similar to the good one."

## Request a Critique

This is a powerful way to find flaws or uncover fresh perspectives. Ask the AI to act as a critic. This can be helpful for important communications and creative assets, like a high-stakes email or finalizing marketing copy.

- "Critique this text from the perspective of a [role, e.g. potential customer]."
- "Play devil's advocate. What is the strongest counter-argument to this?"

## Generate Alternatives

When you're stuck or don't like the direction, ask for options. Use this technique to break through a creative block or explore different angles for your marketing, such as for brainstorming headlines, email subject lines, or calls-to-action.

- "Give me 3 different versions of this."
- "What's an alternative approach to solving this problem?"

## Deepen or Expand on the Initial Output

Use this technique when the output is too shallow. For instance, you can use it to turn a list of bullet points into a detailed paragraph or to add supporting evidence to an argument.

- "Elaborate on point 2."
- "Provide more detail and specific examples for the section about [section]."

---

# Manage More Complex Tasks with Prompt Chaining

When a task is so complex that even a well-phrased prompt isn't enough, prompt chaining – another advanced technique – may be the solution. Instead of trying to craft a perfect standalone prompt on your first try, it's helpful to treat prompting like an ongoing conversation, which is where prompt chaining comes in. This technique is all about thinking of prompting as a way to manage an entire macro-level workflow.

Chaining prompts facilitates large tasks by breaking them into a series of smaller, connected steps within the same chat session. This process functions similarly to an assembly line: the output from one prompt serves as the input for the next, linking each stage together.

This technique involves three key steps:

1. **Task analysis:** Start by breaking down your complex task into a series of smaller, logical steps
2. **Initial prompting:** Craft a focused prompt that asks AI to complete just the first step
3. **Input/output flow:** Use the output from the first prompt as the context for the second prompt, and continue this iterative flow until you complete the task

## A Practical Example

Planning a vacation to Paris requires managing logistics alongside personal interests. Prompt chaining can structure this project through the following sequence.

Here's how prompt chaining could apply to this:

- **Prompt 1:** "I'm going to Paris for 3 days. I like art, historical sites, and parks. Suggest a few well-known places I could visit on my trip."

- **Prompt 2 (second prompt in chain):** "Using those locations, create a logical day-by-day itinerary that minimizes travel time."

- **Prompt 3 (third prompt in chain):** "For each day of the itinerary, suggest a few restaurants located near the suggested locations."

By breaking the task into logical, digestible steps and using the output of one prompt as the specific input for the next, you transform AI from a simple answer generator into a structured collaborator. Another benefit of taking this step by step approach is that it maintains the human-in-the-loop approach. This means you continually verify the AI's output for accuracy at different steps in the process, allowing you to evaluate your prompts and results as you go.

By combining the strategic structure of prompt chaining with the tactical precision of powerful phrases, you move from simply asking questions to truly collaborating with AI on complex projects.
