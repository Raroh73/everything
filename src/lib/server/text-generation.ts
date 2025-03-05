import { pipeline } from "@huggingface/transformers";

export const TextGenerationPipeline = {
  task: "text-generation",
  model: "HuggingFaceTB/SmolLM2-1.7B-Instruct",
  instance: null,

  async getInstance(progress_callback = null) {
    if (this.instance === null) {
      this.instance = pipeline(this.task, this.model, {
        dtype: "q4",
        progress_callback,
      });
    }

    return this.instance;
  },
};
