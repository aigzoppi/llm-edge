import typer
from edgedemo.detection import ImageLoader, PeopleDetector
from edgedemo.inference import InferenceArgs, InferenceRunner

app = typer.Typer()

@app.command()
def run(
    image_path: str = typer.Option('data/images', help="Path to images"),
    number_of_images: int = typer.Option(3, help="Number of images to process"),
    realtime: bool = typer.Option(False, help="Enable realtime mode"),
    enable_inference: bool = typer.Option(False, help="Enable LLM inference integration"),
    model: str = typer.Option('models/bitnet_b1_58-3B/ggml-model-i2_s.gguf', help="Path to model file"),
    n_predict: int = typer.Option(1, help="Number of tokens to predict"),
    threads: int = typer.Option(1, help="Number of threads to use"),
    prompt: str = typer.Option('Describe the image', help="Prompt to send to the model"),
    ctx_size: int = typer.Option(512, help="Context size"),
    temperature: float = typer.Option(0.8, help="Sampling temperature"),
    conversation: bool = typer.Option(False, help="Enable conversation mode"),
):
    loader = ImageLoader(image_path=image_path, realtime=realtime)
    detector = PeopleDetector()
    images, people_counter = detector.detect(loader, number_of_images=number_of_images)
    print(f'\nDirectories.')
    print(f'\nNumber of people recognized = {people_counter}')

    if enable_inference:
        args = InferenceArgs(
            model=model,
            n_predict=n_predict,
            threads=threads,
            prompt=prompt,
            ctx_size=ctx_size,
            temperature=temperature,
            conversation=conversation
        )
        runner = InferenceRunner(args)
        runner.run()
    else:
        print("LLM inference is disabled. Use --enable-inference to enable.")

if __name__ == "__main__":
    app()

