<?php
class UrlParser
{
    public string $path;
    public array $parameters;
    public string $request;
    public function __construct(protected string $url)
    {
        $parsedURL = parse_url($url);
        $this->path = trim(ltrim($parsedURL["path"], "/"));
        $parts = explode("/", $this->path);
        $this->request = array_shift($parts);
        $this->parameters = $parts;
    }
}
