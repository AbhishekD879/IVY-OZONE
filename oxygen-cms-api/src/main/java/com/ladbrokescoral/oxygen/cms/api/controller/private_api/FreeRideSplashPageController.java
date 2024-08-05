package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRideSplashPageRequestDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.FreeRideSplashPageFailureException;
import com.ladbrokescoral.oxygen.cms.api.service.FreeRideSplashPageService;
import java.util.List;
import java.util.Objects;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.web.bind.annotation.*;

@RestController
public class FreeRideSplashPageController extends AbstractCrudController<FreeRideSplashPage> {
  private final ModelMapper modelMapper;
  private final FreeRideSplashPageService service;

  FreeRideSplashPageController(ModelMapper modelMapper, FreeRideSplashPageService service) {
    super(service);
    this.modelMapper = modelMapper;
    this.service = service;
  }

  @PostMapping("/freeride/splashpage")
  public FreeRideSplashPage create(@ModelAttribute @Valid FreeRideSplashPageRequestDto requestDto) {
    String splashPageId = null;
    try {
      FreeRideSplashPage splashpage = modelMapper.map(requestDto, FreeRideSplashPage.class);
      FreeRideSplashPage responseEntity = super.create(splashpage).getBody();
      splashPageId = service.getSplashPageId(responseEntity);
      return service.handleFileUploading(
          splashPageId,
          requestDto.getSplashImg(),
          requestDto.getBannerImg(),
          requestDto.getFreeRideLogoImg());
    } catch (FileUploadException ex) {
      super.delete(splashPageId);
      throw new FreeRideSplashPageFailureException("File Upload Failed");
    } catch (Exception ex) {
      if (Objects.nonNull(splashPageId)) {
        super.delete(splashPageId);
      }
      throw new FreeRideSplashPageFailureException("Error occurred while saving Splash Page");
    }
  }

  @PutMapping("/freeride/splashpage/{id}")
  public FreeRideSplashPage update(
      @PathVariable("id") String id,
      @ModelAttribute @Valid FreeRideSplashPageRequestDto requestDto) {
    try {
      FreeRideSplashPage splashpage =
          super.update(id, modelMapper.map(requestDto, FreeRideSplashPage.class));
      if (!(Objects.isNull(requestDto.getSplashImg())
          && Objects.isNull(requestDto.getBannerImg())
          && Objects.isNull(requestDto.getFreeRideLogoImg()))) {
        splashpage =
            service.handleFileUploading(
                id,
                requestDto.getSplashImg(),
                requestDto.getBannerImg(),
                requestDto.getFreeRideLogoImg());
      }
      return splashpage;
    } catch (FileUploadException ex) {
      throw new FreeRideSplashPageFailureException("File Upload Failed");
    } catch (FreeRideSplashPageFailureException ex) {
      throw new FreeRideSplashPageFailureException("Error occurred while removing image");
    } catch (Exception ex) {
      throw new FreeRideSplashPageFailureException("Error occurred while updating splash page");
    }
  }

  @GetMapping("/freeride/splashpage/brand/{brand}")
  public FreeRideSplashPage getAllSplashPageByBrand(@PathVariable("brand") String brand) {
    List<FreeRideSplashPage> freeRideSplashPageList = service.getFreeRideSplashPageByBrand(brand);
    return !freeRideSplashPageList.isEmpty()
        ? freeRideSplashPageList.get(0)
        : new FreeRideSplashPage();
  }
}
