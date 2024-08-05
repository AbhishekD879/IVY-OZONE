package com.ladbrokescoral.oxygen.cms.api.service.validators;

import com.ladbrokescoral.oxygen.cms.util.ImageUtil;
import java.util.Arrays;
import javax.validation.ConstraintValidator;
import javax.validation.ConstraintValidatorContext;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
public class ImageFileTypeValidator implements ConstraintValidator<ValidFileType, MultipartFile> {

  private String[] validTypes;

  @Override
  public void initialize(ValidFileType constraintAnnotation) {
    validTypes = constraintAnnotation.value();
  }

  @Override
  public boolean isValid(MultipartFile value, ConstraintValidatorContext context) {
    if (value != null) {
      String extension = ImageUtil.getImageExtension(value.getOriginalFilename());
      if (!ImageUtil.isValidType((extension), validTypes)) {
        log.error(
            "Image type '{}' not supported. Supported types are : {}",
            extension,
            Arrays.toString(validTypes));
        context.disableDefaultConstraintViolation();
        context
            .buildConstraintViolationWithTemplate(
                String.format(
                    "file type not supported, supported types are %s", Arrays.toString(validTypes)))
            // .addPropertyNode(extension)
            .addConstraintViolation();
        return false;
      }
    }

    return true;
  }
}
