import { TextGenerationPipeline } from "$lib/server/text-generation";
import { json } from "@sveltejs/kit";
import type { RequestEvent } from "./$types";

export async function POST(event: RequestEvent) {
  const request = await event.request.json();

  const pipe = await TextGenerationPipeline.getInstance();

  const output = await pipe(request.messages, {
    max_new_tokens: request.max_tokens,
  });

  const response = {
    choices: [
      {
        message: output[0].generated_text.at(-1),
      },
    ],
  };

  return json(response);
}
