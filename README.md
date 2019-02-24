# Image Server fith File based cache

- Python 2.7
- Redis 4.0.5
- Flask 1.0.2

## Prerequisites
1. docker
2. docker-compose

## Usage
1. Download/checkout project
2. go to folder
3. run `sudo docker-compose build`
4. run `sudo docker-compose up imageserver`


You can now check at `http://localhost:8000/statistics` for the status

### Image Server
If the size parameter is not present, the server will return the original image
`http://localhost:8000/images/imag2.jpg`

Resized images format
`http://localhost:8000/images/imag2.jpg?size=[WIDTH]x[HEIGHT]`

Adding the size parameter will try to get the image from the cache first,
if it's not found, it will save a copy of the original image at the required size 
on the disk and return it 

The server has some images ready for usage `imag1.jpg` to `imag12.jpg`

## Run Tests
1. Ensure you have a running imageserver, see Usage step
2. go to project folder
3. run `sudo docker-compose up testimageserver`