import typer
from edgedemo.detection import ImageLoader, PeopleDetector

app = typer.Typer()

@app.command()
def run(
    image_path: str = typer.Option('data/images', help="Path to images"),
    number_of_images: int = typer.Option(3, help="Number of images to process"),
    realtime: bool = typer.Option(False, help="Enable realtime mode"),
):
    loader = ImageLoader(image_path=image_path, realtime=realtime)
    detector = PeopleDetector()
    people_counter, crops = detector.detect(loader, number_of_images=number_of_images)
    print(f'\n Number of people recognized = {people_counter}')

if __name__ == "__main__":
    app()

