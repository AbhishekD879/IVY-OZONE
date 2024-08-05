package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.BAD_REQUEST,
    reason = "Could not parse svg image. SVG must have viewBox either width/height attributes")
public class SvgImageParseException extends RuntimeException {}
