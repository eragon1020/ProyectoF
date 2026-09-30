FROM golang:1.22 AS build
WORKDIR /app
COPY go.mod ./
COPY main.go ./
RUN go mod tidy && CGO_ENABLED=0 go build -o server .

FROM gcr.io/distroless/static-debian12
COPY --from=build /app/server /server
CMD ["/server"]
