Maybe someday an 'awesome'-style page... 

# Machine Learning
So-called "Artificial Intelligence"... 🙄

Using the term `localModel`, eg `localGPT` to refer to a model running entirely on a local machine, eg no data exfiltration to cloud.

## Prompt engineering 
I was looking for a guide for LLMs, but works for image generation ala StableDiffusion. Also was fascinated that a text prompt, as an input to Whisper audio transcription can prime it with the topics that are going to be discussed and do a much better job.

> Prompts can be very helpful for correcting specific words or acronyms that the model often misrecognizes in the audio. For example, the following prompt improves the transcription of the words DALL·E and GPT-3, which were previously written as "GDP 3" and "DALI".

- [Prompt Engineering Guide](https://www.promptingguide.ai), ([about section](https://www.promptingguide.ai/about) has more source links)
- [swyx's awesome guide](https://github.com/sw-yx/ai-notes)


## Transcription: Whisper
Interested in where this will go... Two applications: my parent's transcription work, work meetings to auto-generate summaries and action items (via feeding full transcript into a localGPT and asking it questions, perhaps a fixed set and it would be fully automatic, with the option to jump in and ask more later).

TL;DR
— audio in chunks -> log-Mel spectrogram
- encoder: turn audio into tokens
- decoder: turn tokens into English

- [OpenAI's guide for Whisper prompts](https://platform.openai.com/docs/guides/speech-to-text/prompting)
- [Fine tune for multilingual](https://huggingface.co/blog/fine-tune-whisper)
- [Lazy Guide](http://mohitmayank.com/a_lazy_data_science_guide/audio_intelligence/whisper/)

### Running locally

Trialling Hello Transcribe, got Pro ($10) and trialling the .small model (could probably run medium). Crashes. Would be nice if it also recorded the audio, will have to do that and run it separately.

[whisper.cpp](https://github.com/ggerganov/whisper.cpp): the port of Whisper to regular C++ that everyone seems to be using to build on for local apps (read: standalone, not requiring a full ML environment installed). Has optimisations for the Neural Engine on Apple Silicon. Benchmarks: which I don't understand.
[Hello Transcribe](https://www.bjnortier.com/2022/11/01/Say-Hello.html)
[iPhone 14 Pro is faster than a Mac with M1 Pro!](https://twitter.com/bjnortier/status/1643966251188748288)


### Diarisation

Extracting speakers and matching them to chunks of audio. Important for good transcripts. Whisper can't do it directly since it picks a "main speaker" for each chunk and treats the rest as background noise. 

Thought: use side-band stereo or array microphone and a speaker separation toolkit.

Attempts so far seem to match timestamps between PyAnnote and Whiper.

- [Transcription and diarization (speaker identification): Whisper Github conversation](https://github.com/openai/whisper/discussions/264)
- [PyAnnote: Neural building blocks for speaker diarization: speech activity detection, speaker change detection, overlapped speech detection, speaker embedding](https://github.com/pyannote/pyannote-audio)
- [Some code using notebooks in Colab](https://majdoddin.github.io/dyson.html#59.6) and [Sample from a YouTube vid](https://majdoddin.github.io/dyson.html#59.6): autoscrolls with the video timestamp

## Embeddings
Used to extend, finetune models. Important if training something domain-specific.

- [Harnessing OpenAI Embeddings for Advanced NLP: Text Similarity, Semantic Search, and Clustering](https://blog.futuresmart.ai/harnessing-openai-embeddings-for-advanced-nlp-text-similarity-semantic-search-and-clustering)
