package com.ladbrokescoral.oxygen.cms.api.service.validators;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
public class ImageFileSizeValidator implements ConstraintValidator<ValidFileSize, MultipartFile> {

  private long minSize;
  private long maxSize;

  @Override
  public void initialize(ValidFileSize constraintAnnotation) {
    minSize = constraintAnnotation.min();
    maxSize = Long.min(constraintAnnotation.value(), constraintAnnotation.max());
  }

  @Override
  public boolean isValid(MultipartFile value, ConstraintValidatorContext context) {
    if (value != null) {
      long fileSize = value.getSize();
      if (fileSize < minSize) {
        log.error("Image size '{}' less than expected min size: {}", fileSize, minSize);
        context.disableDefaultConstraintViolation();
        context
            .buildConstraintViolationWithTemplate(
                String.format("should be greater than or equal to %d bytes", minSize))
            .addPropertyNode("file size")
            .addConstraintViolation();
        return false;
      }
      if (fileSize > maxSize) {
        log.error("Image size '{}' greater than expected man size: {}", fileSize, maxSize);
        context.disableDefaultConstraintViolation();
        context
            .buildConstraintViolationWithTemplate(
                String.format("should be less than or equal to %d bytes", maxSize))
            .addPropertyNode("file size")
            .addConstraintViolation();
        return false;
      }
    }

    return true;
  }
}
