FROM ubuntu:20.04 as builder

RUN apt-get update && apt-get install clang -y

WORKDIR /src

ARG SECRET_KEY

RUN echo "secret key is ${SECRET_KEY}"

COPY . ./

RUN clang++ -o app app.cpp

FROM ubuntu:20.04

WORKDIR /app

COPY --from=builder /src/app .

CMD ["./app"]
