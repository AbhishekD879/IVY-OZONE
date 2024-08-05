package com.ladbrokescoral.oxygen.cms.api.service;

import static org.assertj.core.api.Java6Assertions.assertThat;
import static org.assertj.core.api.Java6Assertions.assertThatCode;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSport;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTrack;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.VirtualSportTracks;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.exception.FileUploadException;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.VirtualSportTrackRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.*;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class VirtualSportsTrackServiceTest {
  private VirtualSportTrackService service;

  @Mock VirtualSportTrackRepository repository;
  @Mock VirtualSportService virtualSportService;
  @Mock ImageService imageService;

  @Mock SiteServeApiProvider siteServeApiProvider;

  @Mock SiteServerApi siteServerApi;

  VirtualSportTrack virtualSportTrack;
  VirtualSport virtualSport;

  @Mock MultipartFile file;
  String originalFileName = "1.png";

  String virtualsSportTrackImageRootPath = "/root/path/sample";
  String virtualSportTitle = "Virtual Sport";
  String virtualSportTrackTitle = "Virtual Sport Track";
  String trackId = "34543c5a4";

  String expectedPath = "/root/path/sample/virtual-sport/virtual-sport-track/";

  @Mock Filename filenameObjReturnedFromImageService;
  @Mock Filename sameFilenameObj;

  VirtualSportTrack track;

  @Before
  public void setUp() {
    when(file.getOriginalFilename()).thenReturn(originalFileName);

    virtualSport = new VirtualSport();
    virtualSport.setTitle(virtualSportTitle);
    virtualSportTrack = new VirtualSportTrack();
    virtualSportTrack.setTitle(virtualSportTrackTitle);

    track = new VirtualSportTrack();
    track.setId("id");
    track.setTitle("title");
    track.setClassId("321");

    when(repository.findById(trackId)).thenReturn(Optional.of(virtualSportTrack));
    when(virtualSportService.findOne(any())).thenReturn(Optional.of(virtualSport));

    Category category = new Category();
    category.setId(123);
    category.setCategoryName("category name");
    List<Category> classes = Collections.singletonList(category);
    when(siteServerApi.getClasses(any(), any())).thenReturn(Optional.of(classes));
    when(siteServeApiProvider.api(any())).thenReturn(siteServerApi);

    when(imageService.upload(any(), any(), any(), any(), any()))
        .thenReturn(Optional.of(filenameObjReturnedFromImageService));

    service =
        new VirtualSportTrackService(
            virtualsSportTrackImageRootPath,
            repository,
            virtualSportService,
            siteServeApiProvider,
            imageService);
  }

  @Test
  public void testRetrievingClassNameForTrackCreating() {
    service.prepareModelBeforeSave(this.track);

    verify(siteServerApi).getClasses(any(), any());
  }

  @Test(expected = ValidationException.class)
  public void testRetrievingClassNameForClassNotExistingOnSiteServe() {
    when(siteServerApi.getClasses(any(), any())).thenReturn(Optional.empty());

    service.prepareModelBeforeSave(this.track);

    verify(siteServerApi).getClasses(any(), any());
  }

  @Test
  public void testRetrievingClassNameIfClassIdWasNotChanged() {
    VirtualSportTrack updated = new VirtualSportTrack();
    updated.setId("id");
    updated.setTitle("title");
    updated.setClassId("321");

    service.update(this.track, updated);

    verify(siteServerApi, never()).getClasses(any(), any());
  }

  @Test
  public void testRetrievingClassNameIfClassIdChanged() {
    VirtualSportTrack updated = new VirtualSportTrack();
    updated.setId("id");
    updated.setTitle("title");
    updated.setClassId("123");

    service.update(track, updated);

    verify(siteServerApi).getClasses(any(), any());
  }

  @Test
  public void testRemovingImagesOnTitleChange() {
    VirtualSportTrack updated = new VirtualSportTrack();
    updated.setId("id");
    updated.setTitle("NewTitle");
    updated.setClassId("123");
    List<Filename> images = Arrays.asList(new Filename());
    updated.setRunnerImages(images);
    updated.setEventRunnerImages(
        new HashMap<String, List<Filename>>() {
          {
            put("event", images);
          }
        });

    service.update(track, updated);

    assertThat(updated.getRunnerImages().size()).isEqualTo(0);
    assertThat(updated.getEventRunnerImages().size()).isEqualTo(0);
  }

  @Test
  public void testImagesWhenTitleNotChanged() {
    VirtualSportTrack updated = new VirtualSportTrack();
    updated.setId("id");
    updated.setTitle("title");
    updated.setClassId("123");
    List<Filename> images = Arrays.asList(new Filename());
    updated.setRunnerImages(images);
    updated.setEventRunnerImages(
        new HashMap<String, List<Filename>>() {
          {
            put("event", images);
          }
        });

    service.update(track, updated);

    assertThat(updated.getRunnerImages().size()).isEqualTo(1);
    assertThat(updated.getEventRunnerImages().size()).isEqualTo(1);
  }

  public void testFindActiveTracksBySportId() {
    service.findActiveTracksBySportId("365434");

    verify(repository).findBySportIdAndActiveIsTrueOrderBySortOrderAsc("365434");
  }

  @Test
  public void testCallToImageServiceOnFirstImageUploading() {
    service.attachImage(trackId, file, null);

    ArgumentCaptor<MultipartFile> fileForImageCaptor = ArgumentCaptor.forClass(MultipartFile.class);
    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<String> nameForImageCaptor = ArgumentCaptor.forClass(String.class);

    verify(imageService)
        .upload(
            any(),
            fileForImageCaptor.capture(),
            pathForImageCaptor.capture(),
            nameForImageCaptor.capture(),
            any());
    assertThat(file).isEqualTo(fileForImageCaptor.getValue());
    assertThat(expectedPath).isEqualTo(pathForImageCaptor.getValue());
    assertThat("1").isEqualTo(nameForImageCaptor.getValue());

    verify(imageService, never()).removeImage(any(), any());
  }

  @Test
  public void testCallToImageServiceOnFirstImageUploadingForEvent() {
    String eventName = "test-event";
    service.attachImage(trackId, file, eventName);

    ArgumentCaptor<MultipartFile> fileForImageCaptor = ArgumentCaptor.forClass(MultipartFile.class);
    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<String> nameForImageCaptor = ArgumentCaptor.forClass(String.class);

    verify(imageService)
        .upload(
            any(),
            fileForImageCaptor.capture(),
            pathForImageCaptor.capture(),
            nameForImageCaptor.capture(),
            any());
    assertThat(file).isEqualTo(fileForImageCaptor.getValue());
    assertThat(expectedPath + eventName).isEqualTo(pathForImageCaptor.getValue());
    assertThat("1").isEqualTo(nameForImageCaptor.getValue());

    verify(imageService, never()).removeImage(any(), any());
  }

  @Test
  public void testSavingProperFieldsInRepositoryOnImageUploading() {
    service.attachImage(trackId, file, null);

    ArgumentCaptor<VirtualSportTrack> sportTrackCaptor =
        ArgumentCaptor.forClass(VirtualSportTrack.class);

    verify(repository).save(sportTrackCaptor.capture());
    Filename filename = sportTrackCaptor.getValue().getRunnerImages().get(0);
    assertThat(filenameObjReturnedFromImageService).isEqualTo(filename);
  }

  @Test(expected = FileUploadException.class)
  public void testThrowingExceptionOnImageUploadingFailure() {
    when(imageService.upload(any(), any(), any(), any(), any())).thenReturn(Optional.empty());

    service.attachImage(trackId, file, null);
  }

  @Test
  public void testUploadingSameNameAttachedImage() {

    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    virtualSportTrack.setRunnerImages(Collections.singletonList(sameFilenameObj));

    service.attachImage(trackId, file, null);

    verify(imageService).removeImage(any(), any());
    verify(imageService).upload(any(), any(), any(), any(), any());
    verify(repository).save(any(VirtualSportTrack.class));
  }

  @Test
  public void testUploadingSameNameAttachedImageForEvent() {
    String eventName = "test-event";

    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    virtualSportTrack
        .getEventRunnerImages()
        .put(eventName, Collections.singletonList(sameFilenameObj));

    service.attachImage(trackId, file, eventName);

    verify(imageService).removeImage(any(), any());
    verify(imageService).upload(any(), any(), any(), any(), any());
    verify(repository).save(any(VirtualSportTrack.class));
    assertThat(virtualSportTrack.getEventAliases()).containsOnlyKeys(eventName);
  }

  @Test(expected = FileUploadException.class)
  public void testUploadingSameNameAttachedImageFailedOnRemovingPrevious() {
    when(imageService.removeImage(any(), any())).thenReturn(false);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    virtualSportTrack.setRunnerImages(Collections.singletonList(sameFilenameObj));

    service.attachImage(trackId, file, null);

    verify(imageService).removeImage(any(), any());
    verify(imageService, never()).upload(any(), any(), any(), any(), any());
    verify(repository, never()).save(any(VirtualSportTrack.class));
  }

  @Test
  public void testRemovingAttachedImageByFullPath() {
    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    String fullPathSample = "full/path/1.png";
    when(sameFilenameObj.getFullPath()).thenReturn(fullPathSample);
    virtualSportTrack.setRunnerImages(new ArrayList<>(Collections.singletonList(sameFilenameObj)));

    service.removeImageForVirtualSportTrack(
        trackId,
        new VirtualSportTracks.SingleForTrackRemoveImageRequest().setFilename(originalFileName));

    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    verify(imageService).removeImage(any(), pathForImageCaptor.capture());
    assertThat(fullPathSample).isEqualTo(pathForImageCaptor.getValue());

    ArgumentCaptor<VirtualSportTrack> sportTrackCaptor =
        ArgumentCaptor.forClass(VirtualSportTrack.class);
    verify(repository).save(sportTrackCaptor.capture());
    assertThat(sportTrackCaptor.getValue().getRunnerImages()).isEmpty();
  }

  @Test
  public void testRemovingSingleImageForEvent() {
    String eventSample = "test-event";
    String fullPathSample = "parent/child/event/1.png";
    Filename otherFileStub = new Filename();
    otherFileStub.setFilename("other.png");

    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    when(sameFilenameObj.getFullPath()).thenReturn(fullPathSample);
    virtualSportTrack
        .getEventRunnerImages()
        .put(
            eventSample,
            new ArrayList<>(Arrays.asList(otherFileStub, sameFilenameObj, otherFileStub)));
    virtualSportTrack.getEventAliases().put(eventSample, eventSample);

    service.removeImageForVirtualSportTrack(
        trackId,
        new VirtualSportTracks.SingleForEventRemoveImageRequest()
            .setEvent(eventSample)
            .setFilename(originalFileName));

    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    verify(imageService).removeImage(any(), pathForImageCaptor.capture());
    assertThat(fullPathSample).isEqualTo(pathForImageCaptor.getValue());

    verify(repository).save(any(VirtualSportTrack.class));
    assertThat(virtualSportTrack.getEventAliases().get(eventSample)).isNotBlank();
    assertThat(virtualSportTrack.getEventRunnerImages().get(eventSample))
        .doesNotContain(sameFilenameObj)
        .hasSize(2);
  }

  @Test
  public void testRemovingSingleImageForEventNoneLeft() {
    String eventSample = "test-event";
    String fullPathSample = "parent/child/event/1.png";

    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    when(sameFilenameObj.getFullPath()).thenReturn(fullPathSample);
    virtualSportTrack
        .getEventRunnerImages()
        .put(eventSample, new ArrayList<>(Collections.singletonList(sameFilenameObj)));
    virtualSportTrack.getEventAliases().put(eventSample, eventSample);

    service.removeImageForVirtualSportTrack(
        trackId,
        new VirtualSportTracks.SingleForEventRemoveImageRequest()
            .setEvent(eventSample)
            .setFilename(originalFileName));

    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    verify(imageService).removeImage(any(), pathForImageCaptor.capture());
    assertThat(fullPathSample).isEqualTo(pathForImageCaptor.getValue());

    verify(repository).save(any(VirtualSportTrack.class));
    assertThat(virtualSportTrack.getEventAliases().get(eventSample)).isNull();
    assertThat(virtualSportTrack.getEventRunnerImages().get(eventSample)).isEmpty();
  }

  @Test
  public void testRemovingAllImagesForEvent() {
    String eventSample = "test-event";
    String fullPathSample = "parent/child/event/1.png";
    Filename otherFileStub = new Filename();
    otherFileStub.setFilename("other.png");

    when(imageService.removeImage(any(), any())).thenReturn(true);
    when(sameFilenameObj.getFullPath()).thenReturn(fullPathSample);
    virtualSportTrack
        .getEventRunnerImages()
        .put(
            eventSample,
            new ArrayList<>(Arrays.asList(otherFileStub, sameFilenameObj, otherFileStub)));
    virtualSportTrack.getEventAliases().put(eventSample, eventSample);

    service.removeImageForVirtualSportTrack(
        trackId, new VirtualSportTracks.AllForEventRemoveImageRequest().setEvent(eventSample));
    ArgumentCaptor<String> pathForImageCaptor = ArgumentCaptor.forClass(String.class);
    verify(imageService, times(3)).removeImage(any(), pathForImageCaptor.capture());
    assertThat(fullPathSample).isEqualTo(pathForImageCaptor.getAllValues().get(1));

    verify(repository).save(any(VirtualSportTrack.class));
    assertThat(virtualSportTrack.getEventAliases().get(eventSample)).isNull();
    assertThat(virtualSportTrack.getEventRunnerImages().get(eventSample)).isNull();
  }

  @Test(expected = FileUploadException.class)
  public void testRemovingAttachedImageByFullPathThrowsExceptionOnFailure() {
    when(imageService.removeImage(any(), any())).thenReturn(false);
    when(sameFilenameObj.getFilename()).thenReturn(originalFileName);
    String fullPathSample = "full/path/1.png";
    when(sameFilenameObj.getFullPath()).thenReturn(fullPathSample);
    virtualSportTrack.setRunnerImages(new ArrayList<>(Collections.singletonList(sameFilenameObj)));

    service.removeImageForVirtualSportTrack(
        trackId,
        new VirtualSportTracks.SingleForTrackRemoveImageRequest().setFilename(originalFileName));
  }

  @Test
  public void testRemovingImagesFotVirtualSportTrack() {
    when(imageService.removeImage(any(), any())).thenReturn(true);
    Filename otherFile = new Filename();
    otherFile.setFilename("other");
    virtualSportTrack.setRunnerImages(new ArrayList<>(Arrays.asList(sameFilenameObj, otherFile)));

    service.removeInCloudImagesForVirtualSportTrack(virtualSportTrack);

    verify(imageService, times(2)).removeImage(any(), any());
  }

  @Test
  public void testRemovingImagesForVirtualSportTrackFailsToRemoveImage() {
    when(imageService.removeImage(any(), any())).thenReturn(false);
    Filename otherFile = new Filename();
    otherFile.setFilename("other");

    virtualSportTrack.setRunnerImages(new ArrayList<>(Arrays.asList(sameFilenameObj, otherFile)));
    assertThatCode(() -> service.removeInCloudImagesForVirtualSportTrack(virtualSportTrack))
        .doesNotThrowAnyException();
  }
}
