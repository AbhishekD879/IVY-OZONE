package com.ladbrokescoral.oxygen.cms.api.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

@ResponseStatus(
    value = HttpStatus.FORBIDDEN,
    reason = "You have no right to update or delete this section")
public class SectionUpdatingOrDeletingForbidden extends RuntimeException {}