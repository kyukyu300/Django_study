from io import BytesIO

from PIL import Image
from pathlib import Path
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

from utils.models import TimestampModel

User = get_user_model()

class Blog(TimestampModel):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('music', '음악'),
        ('game', '게임'),
        ('study', '공부'),
    )
    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES, default='free')
    title = models.CharField('제목',max_length=100)
    content = models.TextField('본문')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image = models.ImageField('이미지', null= True, blank= True, upload_to='blog/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='blog/%Y/%m/%d')
    # CASCADE => 깉이 삭제
    # PROTECT => 삭제 불가능
    # SET_NULL => author가 null 처리 됨
    # created_at = models.DateTimeField('작성일자', auto_now_add=True)
    # updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'blog_pk': self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300,300))

        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension in '.gif':
            file_type = 'GIF'
        elif thumbnail_extension in '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)




    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

class Comment(TimestampModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField('본문', max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.blog.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id')