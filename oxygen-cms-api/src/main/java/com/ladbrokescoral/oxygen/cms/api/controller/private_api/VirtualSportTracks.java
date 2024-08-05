package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualSportTrackService;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class VirtualSportTracks extends AbstractSortableController<VirtualSportTrack> {
  private final VirtualSportTrackService virtualSportTrackService;

  VirtualSportTracks(VirtualSportTrackService virtualSportTrackService) {
    super(virtualSportTrackService);
    this.virtualSportTrackService = virtualSportTrackService;
  }

  @Override
  @GetMapping("/virtual-sport-track")
  public List<VirtualSportTrack> readAll() {
    return super.readAll();
  }

  @GetMapping("virtual-sport-track/sport-id/{sportId}")
  public List<VirtualSportTrack> readBySportId(@PathVariable String sportId) {
    return virtualSportTrackService.findBySportId(sportId);
  }

  @Override
  @PostMapping("virtual-sport-track/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @Override
  @PostMapping("/virtual-sport-track")
  public ResponseEntity create(@Valid @RequestBody VirtualSportTrack entity) {
    return super.create(entity);
  }

  @Override
  @GetMapping("/virtual-sport-track/{id}")
  public VirtualSportTrack read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PutMapping("/virtual-sport-track/{id}")
  public VirtualSportTrack update(
      @PathVariable("id") String id, @Valid @RequestBody VirtualSportTrack updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("/virtual-sport-track/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    Optional<VirtualSportTrack> mayBeVirtualSportTrack = crudService.findOne(id);
    mayBeVirtualSportTrack.ifPresent(
        this.virtualSportTrackService::removeInCloudImagesForVirtualSportTrack);

    return delete(mayBeVirtualSportTrack);
  }

  @PostMapping("virtual-sport-track/{id}/image-upload")
  public VirtualSportTrack uploadImage(
      @PathVariable("id") String id,
      @RequestParam("file") MultipartFile icon,
      @NotBlank @RequestParam(value = "event", required = false) String eventName) {
    return virtualSportTrackService.attachImage(id, icon, eventName);
  }

  @PostMapping("virtual-sport-track/{id}/image-remove")
  public ResponseEntity<VirtualSportTrack> removeImage(
      @PathVariable("id") String id, @RequestBody RemoveImageRequest removeImageRequest) {
    VirtualSportTrack virtualSportTrack =
        virtualSportTrackService.removeImageForVirtualSportTrack(id, removeImageRequest);
    return new ResponseEntity<>(virtualSportTrack, HttpStatus.OK);
  }

  @JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
  @JsonSubTypes({
    @JsonSubTypes.Type(value = AllForEventRemoveImageRequest.class, name = "ALL_FOR_EVENT"),
    @JsonSubTypes.Type(value = SingleForEventRemoveImageRequest.class, name = "SINGLE_FOR_EVENT"),
    @JsonSubTypes.Type(value = SingleForTrackRemoveImageRequest.class, name = "SINGLE_FOR_TRACK"),
  })
  public interface RemoveImageRequest {

    @JsonIgnore
    List<Filename> imagesToRemove(VirtualSportTrack track);
  }

  @Data
  @Accessors(chain = true)
  public static class AllForEventRemoveImageRequest implements RemoveImageRequest {
    private String event;

    @Override
    public List<Filename> imagesToRemove(VirtualSportTrack track) {
      List<Filename> imagesToRemove = track.getEventRunnerImages().get(event);

      track.getEventRunnerImages().remove(event);
      track.getEventAliases().remove(event);

      return imagesToRemove;
    }
  }

  @Data
  @Accessors(chain = true)
  public static class SingleForEventRemoveImageRequest implements RemoveImageRequest {
    private String event;
    private String filename;

    @Override
    public List<Filename> imagesToRemove(VirtualSportTrack track) {
      List<Filename> imagesToRemove =
          track.getEventRunnerImages().get(event).stream()
              .filter(image -> image.getFilename().equals(filename))
              .collect(Collectors.toList());

      track
          .getEventRunnerImages()
          .get(event)
          .removeIf(image -> image.getFilename().equals(filename));

      if (track.getEventRunnerImages().get(event).isEmpty()) {
        track.getEventAliases().remove(event);
      }
      return imagesToRemove;
    }
  }

  @Data
  @Accessors(chain = true)
  public static class SingleForTrackRemoveImageRequest implements RemoveImageRequest {
    private String filename;

    @Override
    public List<Filename> imagesToRemove(VirtualSportTrack track) {
      List<Filename> imagesToRemove =
          track.getRunnerImages().stream()
              .filter(image -> image.getFilename().equals(filename))
              .collect(Collectors.toList());

      track.getRunnerImages().removeIf(image -> image.getFilename().equals(filename));

      return imagesToRemove;
    }
  }
}
