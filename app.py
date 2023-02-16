import asyncio
import datetime
import json
import os
import re
import subprocess
from flet import *
from pytube import YouTube
import requests
height = 890
width = 1500
br=30
drag_height = 50
base_color = '#262d31'
close_color = '#ff994f'
max_color = '#87e897'
tabs_color = '#30434e'
tabs_grey  = '#5a6b74'
tabs_grey2  = '#384b55'
tabs_grey3  = '#455761'
tabs_br = 25
tabs_height = 150
title_border = border.only(right=border.BorderSide(width=2,color=tabs_grey,))
base_animation = animation.Animation(400,AnimationCurve.DECELERATE)
base_animation2 = animation.Animation(200,AnimationCurve.EASE_OUT)


class WindowDrag(UserControl):
  def __init__(self,color):
    super().__init__()
    self.color = color
  def build(self):
    return Container(content=WindowDragArea(height=10,content=Container(bgcolor=self.color)))

class DownloadItem(GestureDetector):
  def __init__(self,filename,filesize,status):
    super().__init__()
    
    self.on_double_tap=self.open_file_explorer

    self.content=Container(
        padding = padding.symmetric(horizontal=20),
        height=100,
        border=border.only(bottom=border.BorderSide(width=2.5,color=tabs_grey)),
        bgcolor='#6630434e',
        content=Row(
          spacing = 20,
          controls=[
            Container(
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              expand = True,
              content=Row(
                controls=[
                  Image(
                    src='mp4.png',
                    # scale=0.4,
                  ),
                  Text(
                    value=filename,
                    font_family='montserrat medium',
                    size=14,
                  ),
                ]
              )
            ),
            Container(
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              width = 100,
              content=Text(
                value=None,
                font_family='montserrat medium',
                size=14,
              ),
            ),
            Container(
              width = 120,
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              
              content=Text(
                value=status,
                font_family='montserrat medium',
                size=14,
              ),
            ),
            Container(
              clip_behavior=ClipBehavior.ANTI_ALIAS,
              
              width = 100,
              content=Text(
                value=filesize,
                font_family='montserrat medium',
                size=14,
              ),
            ),
          ]
        )
      )

  def open_file_explorer(self,e: TapEvent):
    file_path = r"E:\1597811_Capture.png"
    subprocess.run(['explorer', '/select,', file_path])
    

class ResItem(Container):
  def __init__(self,label,data,url,filename):
    super().__init__()
    self.download_ongoing = True

    self.content = Container(
      
      padding=padding.only(right=20),
      height=50, bgcolor=tabs_grey,
      content=Row(
        alignment='spaceBetween',
        controls=[
          Radio(value=label, label=label,fill_color=tabs_color),
          Text(value=data,)
    ]))


class Main(UserControl):
  def __init__(self,pg:Page):
    pg.fonts = {
    "Poppins ThinItalic":"fonts/poppins/Poppins-ThinItalic.ttf",
    "Poppins Thin":"fonts/poppins/Poppins-Thin.ttf",
    "Poppins Semibold":"fonts/poppins/Poppins-Semibold.ttf",
    "Poppins SemiboldItalic":"fonts/poppins/Poppins-SemiboldItalic.ttf",
    "Poppins Regular":"fonts/poppins/Poppins-Regular.ttf",
    "Poppins MediumItalic":"fonts/poppins/Poppins-MediumItalic.ttf",
    "Poppins Medium":"fonts/poppins/Poppins-Medium.ttf",
    "Poppins LightItalic":"fonts/poppins/Poppins-LightItalic.ttf",
    "Poppins Light":"fonts/poppins/Poppins-Light.ttf",
    "Poppins Italic":"fonts/poppins/Poppins-Italic.ttf",
    "Poppins ExtraLightItalic":"fonts/poppins/Poppins-ExtraLightItalic.ttf",
    "Poppins ExtraLight":"fonts/poppins/Poppins-ExtraLight.ttf",
    "Poppins ExtraBold":"fonts/poppins/Poppins-ExtraBold.ttf",
    "Poppins ExtraBoldItalic":"fonts/poppins/Poppins-ExtraBoldItalic.ttf",
    "Poppins BoldItalic":"fonts/poppins/Poppins-BoldItalic.ttf",
    "Poppins Bold":"fonts/poppins/Poppins-Bold.ttf",
    "Poppins BlackItalic":"fonts/poppins/Poppins-BlackItalic.ttf",
    "Poppins Black":"fonts/poppins/Poppins-Black.ttf",
    "Montserrat Black":"fonts/montserrat/Montserrat-Black.ttf",
    "Montserrat Light":"fonts/montserrat/Montserrat-Light.ttf",
    "Montserrat Medium":"fonts/montserrat/Montserrat-Medium.ttf",
    "Montserrat Regular":"fonts/montserrat/Montserrat-Regular.ttf",
    "Montserrat Bold":"fonts/montserrat/Montserrat-Bold.ttf",
  }
    pg.window_height = height
    pg.window_width = width
    pg.window_bgcolor = colors.TRANSPARENT
    pg.bgcolor = colors.TRANSPARENT
    pg.window_title_bar_hidden =True
    pg.window_frameless = True
    
    self.pg = pg

    
    self.init_helper()
    self.load_history()


  def init_helper(self):
    self.download_items_column = Column(
      height=470,
      scroll='auto',
      controls=[
        
      ]
    )

                
    self.resolution_items_column = Column(
      height=440,
      scroll='auto',
      controls=[
        
      ]
    )    


    self.reses_group = RadioGroup(
      content=self.resolution_items_column,
    )           


    self.choose_resolution = Container(
      animate=base_animation,
      offset=transform.Offset(0,2),
      animate_offset=base_animation2,
      top=275,
      left=280,
      width=800,
      height=570,
      bgcolor='#101a1f',
      border_radius=br,
      border=border.all(width=2.3,color=tabs_color),
      padding = 20,
      content=Column(
        horizontal_alignment='center',
        controls=[
          Text(
            value='Please choose a resolution',
            size=20,
            font_family='montserrat medium'
          ),
          self.reses_group,
          Row(
            alignment='end',
            controls=[
              Container(
                on_click=self.start_download,
                height=40,width=120,bgcolor=tabs_color,alignment=alignment.center,
                content=Text('Start Download',size=14,weight='bold')
              ),
              Container(
                on_click=self.cancelled,
                height=40,width=120,bgcolor=tabs_color,alignment=alignment.center,
                content=Text('Cancel',size=14,weight='bold')
              )
            ]
          )

        ]
      )
    )


    
    self.url_input = Card(
              top=300,
              left=500,
              height=150,
              width=600,
              elevation=10,
              content=Container(
                padding=30,
                bgcolor='white',
                content=Column(
                  alignment='center',
                  horizontal_alignment='center',
                  controls=[
                    Text(
                      value='Please paste your URL below'.upper(),
                      size=22,
                      color='#5d6e77',
                      font_family='montserrat bold'
                    ),
                    Row(
                      controls=[
                        Container(
                          expand=True,
                          bgcolor='#98a6ac',
                          content=TextField(
                            border=InputBorder.NONE,
                            content_padding=10,
                            hint_text='Paste URL in this box',
                            hint_style=TextStyle(
                              size=14,color='#5d6e77',
                              
                            ),
                            text_style=TextStyle(
                              size=18,color='#5d6e77',
                              font_family='montserrat medium',

                              
                            )
                          )
                        ),
                        Container(
                          on_click=self.extract_clicked,
                          height=50,
                          width=80,
                          bgcolor='#5d6e77',
                          content=Text(
                            value='Extract',
                            font_family='montserrat medium',
                            size=18
                          ),
                          alignment=alignment.center
                        )
                      ]
                    )
                  ]
                )
              )
            )
    

    self.loading_animation = Card(
      top=180,
      left=400,
      height=370,
      width=600,
      elevation=10,
      content=Container(
        padding=25,
        content=Column(

          horizontal_alignment='center',
          controls=[
            Text(
              'Please wait, fetching url details...',
              size=18,

            ),
            Image(
              src='loading.gif'
            )
          ]
        )
      )
    )


    self.main_content = Container(
              expand=True,
              content=Column(
                spacing=0,
                controls=[
                  Container(
                    height=drag_height+25,
                    content=WindowDragArea(
                      content=Container(
                        margin=margin.only(top=25),
                        content=Row(
                          alignment='spaceBetween',
                          controls=[
                            Row(
                              spacing=20,
                              controls=[
                                Container(
                                  height=45,width=45,
                                  # bgcolor='white',
                                  # border_radius=30,
                                  content=Image(
                                    src='logo.png'
                                  )

                                ),
                                Container(
                                  on_hover=self.hover_handler,
                                  bgcolor=None,
                                  content=Text(
                                    value='Tasks',
                                    size=18
                                  ),
                                ),
                                Container(
                                  bgcolor=None,
                                  content=Text(
                                    value='File',
                                    size=18
                                  ),
                                ),
                                Container(
                                  bgcolor=None,
                                  content=Text(
                                    value='View',
                                    size=18
                                  ),
                                ),
                                Container(
                                  bgcolor=None,
                                  content=Text(
                                    value='Help',
                                    size=18
                                  ),
                                ),
                              ]
                            ),
                            Text(
                              value='All Media Downloader',
                              size=20,
                            ),
                            Row(
                              width=120,
                              alignment='spaceBetween',
                              controls=[
                                Container(
                                  height=5,
                                  width=22,
                                  bgcolor='white',
                                  border_radius=2,
                                ),
                                Container(
                                  height=22,
                                  width=22,
                                  bgcolor=max_color,
                                  border_radius=7,
                                ),
                                Container(
                                  height=22,
                                  width=22,
                                  bgcolor=close_color,
                                  border_radius=7,
                                  rotate=45
                                ),
                              ]
                            )
                          ]
                        )

                      )
                    )
                  ),

                  Container(height=20),

                  Container(
                    content=Row(
                      spacing=30,
                      controls=[
                        Container(
                          on_click=self.open_url_dlg,
                          height=tabs_height,
                          width=260,
                          bgcolor=tabs_color,
                          border_radius=br,
                          content=Row(
                            spacing=15,
                            alignment='center',
                            controls=[
                              Container(
                                height=70,
                                width=70,
                                border_radius=15,
                                bgcolor=tabs_grey,
                                content=Image(
                                  src='plus.png',
                                  scale=0.5
                                )
                              ),
                              Text(
                                value='Add URL',
                                font_family='montserrat medium',
                                size=20,
                              )
                            ]
                          )

                        ),
                        
                        Container(
                          padding = 25,
                          height=tabs_height,
                          width=360,
                          bgcolor=tabs_color,
                          border_radius=br,
                          content=Row(
                            spacing=20,
                            controls=[
                              Text(
                                value='Download Controller',
                                width=120,
                                size=20,
                                font_family='montserrat regular'
                              ),
                              Container(
                                height=80,
                                width=80,
                                bgcolor=tabs_grey2,
                                border_radius=40,
                                content=Image(
                                  src='play.png'
                                )
                              ),
                              
                              Container(
                                height=80,
                                width=80,
                                bgcolor=tabs_grey2,
                                border_radius=40,
                                content=Row(
                                  alignment='center',
                                  controls=[
                                    Container(
                                      height=30,width=30,border_radius=5,
                                      bgcolor=tabs_grey3,
                                    )
                                  ]
                                )
                              ),
                            ]
                          )
                        ),
                        
                        Container(
                          height=tabs_height,
                          width=250,
                          bgcolor=tabs_color,
                          border_radius=br,
                          padding = 20,
                          content=Row(
                            controls=[
                              Container(
                                width=100,
                                content=Column(
                                  horizontal_alignment='center',
                                  alignment='center',
                                  controls=[
                                    Image(
                                      src='trash.png',
                                      # scale=0.5
                                    ),
                                    Text(
                                      value='Delete',
                                      font_family='montserrat regular',
                                      size=14
                                    )
                                  ]
                                )
                              ),
                              
                              Container(
                                width=100,
                                content=Column(
                                  # horizontal_alignment='center',
                                  alignment='center',
                                  controls=[
                                    Row(
                                      vertical_alignment='end',
                                      spacing=0,
                                      controls=[
                                        Image(
                                          src='trash.png',
                                        ),
                                        Image(
                                          src='trash1.png',
                                        )
                                      ]
                                    ),
                                    Text(
                                      value='Delete All',
                                      font_family='montserrat regular',
                                      size=14
                                    )
                                  ]
                                )
                              ),
                              
                            ]
                          )
                        ),
                        
                        Container(
                          height=tabs_height,
                          width=300,
                          bgcolor=tabs_color,
                          border_radius=br,
                          content=Row(
                            alignment='center',
                            controls=[
                              Container(
                                width=100,
                                content=Column(
                                  horizontal_alignment='center',
                                  alignment='center',
                                  controls=[
                                    Image(
                                      src='add_queue.png',
                                      # scale=0.5
                                    ),
                                    Text(
                                      value='Add Queue',
                                      font_family='montserrat regular',
                                      size=14
                                    )
                                  ]
                                )
                              ),
                              
                              Container(
                                width=100,
                                content=Column(
                                  horizontal_alignment='center',
                                  alignment='center',
                                  controls=[
                                   
                                    Image(
                                      src='stop_queue.png',
                                    ),
                                    Text(
                                      value='Stop Queue',
                                      font_family='montserrat regular',
                                      size=14
                                    )
                                  ]
                                )
                              ),
                              
                            ]
                          )
                        ),
                        
                        Container(
                          height=tabs_height,
                          width=150,
                          padding=7,
                          border_radius=br,
                          content=Column(
                            alignment='spaceBetween',
                            spacing = 0,
                            horizontal_alignment='center',
                            controls=[
                              Image(
                                src='setting.png',
                              ),
                              Text(
                                value='Options',
                                font_family='montserrat regular'
                              )
                            ]
                          )
                        ),
                      ]
                    )
                  ),
                  Container(height=30),

                  Container(
                    expand=True,
                    content=Row(
                      spacing = 30,
                      controls=[
                        Container(
                          width=260,
                          # bgcolor='red',
                          border=border.all(width=2.3,color=tabs_color),
                          border_radius=br,
                          padding=20,
                          content=Column(
                            controls=[
                              Text(
                                value='Categories',
                                font_family='montserrat medium',
                                size=25,
                                color=tabs_grey
                              ),
                              # Container(height=30),
                              Container(
                                # padding=padding.only(left=20),
                                content=Column(
                                  controls=[
                                    Container(
                                      alignment=alignment.center,
                                      # padding=12,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='All Downloads',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      alignment=alignment.center,
                                      # padding=12,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='Compressed',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      alignment=alignment.center,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='Programs',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      alignment=alignment.center,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='Documents',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      alignment=alignment.center,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='Videos',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      
                                      alignment=alignment.center,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      content=Text(
                                        value='Music',
                                        size=18,
                                      )
                                    ),
                                    Container(
                                      alignment=alignment.center,
                                      bgcolor=tabs_grey,
                                      height=50,
                                      width=200,
                                      # expand=True,
                                      content=Text(
                                        value='Picture',
                                        size=18,
                                      )
                                    ),
                                  ]
                                )
                              ),
                            ]
                          )
                        ),

                        Container(
                          expand=True,
                          bgcolor='#101a1f',
                          border_radius=br,
                          border=border.all(width=2.3,color=tabs_color),
                          padding = 20,
                          content=Column(
                            controls=[
                              Container(
                                padding = padding.symmetric(horizontal=20),
                                height=60,
                                border_radius=20,
                                bgcolor=tabs_color,
                                content=Row(
                                  spacing = 20,
                                  controls=[
                                    Container(
                                      # width = 300,
                                      expand = True,
                                      border = title_border,
                                      content=Text(
                                        value='Filename',
                                        font_family='montserrat medium',
                                        size=14,
                                      ),
                                    ),
                                    Container(
                                      width = 100,
                                      border = title_border,
                                      content=Text(
                                        value='Transfer rate',
                                        font_family='montserrat medium',
                                        size=14,
                                      ),
                                    ),
                                    Container(
                                      width = 120,
                                      border = title_border,
                                      content=Text(
                                        value='Status',
                                        font_family='montserrat medium',
                                        size=14,
                                      ),
                                    ),
                                    Container(
                                      # border = title_border,
                                      width = 100,
                                      content=Text(
                                        value='File size',
                                        font_family='montserrat medium',
                                        size=14,
                                      ),
                                    ),

                                  ]
                                )
                              ),

                              self.download_items_column,
                            ]
                          )
                        )
                      ]
                    )
                  )
                ]
              )
            )
                    

    self.window_main_content = Stack(
        expand=True,
          controls=[
            self.main_content,
            self.choose_resolution,
            # self.url_input,
            # self.loading_animation,
          ]
        )            
    
    self.pg.add(
      Container(
        clip_behavior=ClipBehavior.ANTI_ALIAS,
        expand=True,
        border_radius=br,
        padding=padding.only(bottom=25,right=25,left=25),
        bgcolor=base_color,
        content=self.window_main_content,

        
      )
    )
    
  def hover_handler(self,e:HoverEvent):
    # self.pg.launch_url()
    default_bg = e.control.bgcolor
    # if e.data == 'true':
    #   e.control.bgcolor = 'red'
    # else:
    #   e.control.bgcolor = default_bg
    # e.control.update()
    

  def open_url_dlg(self,e):
    if isinstance(self.pg.get_clipboard(), str):
      url = self.pg.get_clipboard()
    
      if not self.is_valid_url(url):
        for c in self.main_content.content.controls[1:]:
          c.opacity = 0.05
          c.update()
        self.window_main_content.controls.insert(1,self.url_input) 
        self.window_main_content.update()
      else:
        for c in self.main_content.content.controls[1:]:
          c.opacity = 0.05
          c.update()
        self.window_main_content.controls.insert(1,self.loading_animation) 
        self.window_main_content.update()
        url = requests.get(url).url
        yt = YouTube(url)
        temp_res = []
        self.details_fetched = {

        }
        for res in yt.streams:
          if res.resolution and res.resolution not in temp_res:
            temp_res.append(res.resolution)
            self.details_fetched[res.resolution.upper()] ={
                                                            "filename": yt.title,
                                                            "size": self.convert_bytes(res.filesize),
                                                            "url": url,
                                                            "download_from": "youtube",
                                                            "status": "pending",
                                                            "direct_link":res.url,
                                                            "needs_merge":False,
                                                            "type":"mp4",
                                                            "create_date":str(datetime.datetime.utcnow().date()),
                                                            "cookie":'None',
                                                            "time_left":'None',
                                                            "res":res.resolution.upper(),
                                                            "downloaded":'None'
                                                          }
            self.resolution_items_column.controls.append(
              ResItem(res.resolution.upper(), self.convert_bytes(res.filesize), res.url, yt.title)
            )
        self.window_main_content.controls.remove(self.loading_animation) 
        self.window_main_content.update()

        self.resolution_items_column.update()  
        self.choose_resolution.offset.y = 0
        self.choose_resolution.update()
        



  def reset_view(self,):
    self.resolution_items_column.controls.clear()
    self.choose_resolution.offset.y = 2
    self.resolution_items_column.update()
    self.choose_resolution.update()
    for c in self.main_content.content.controls[1:]:
      c.opacity = 1
      c.update()


  def extract_clicked(self,e: TapEvent):
    self.reset_view()
    self.window_main_content.controls.remove(self.url_input) 
    self.window_main_content.update()  


  def is_valid_url(self,url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https:// or ftp:// or ftps://
        r'(?:(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}))'  # IPv4 address
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(regex.match(url))


  def open_file_explorer(self,e: TapEvent):
    file_path = r"E:\1597811_Capture.png"
    subprocess.run(['explorer', '/select,', file_path])
    

  async def fetch_direct_links(self,url):
    print(url)  

  def convert_bytes(self,size_bytes):
    """
    Convert a byte value to the nearest kilobyte (KB), megabyte (MB), or gigabyte (GB).
    """
    # define the unit sizes
    KB = 1024
    MB = KB ** 2
    GB = KB ** 3

    # determine the appropriate unit size
    if size_bytes >= GB:
        size = f"{size_bytes / GB:.2f} GB"
    elif size_bytes >= MB:
        size = f"{size_bytes / MB:.2f} MB"
    elif size_bytes >= KB:
        size = f"{size_bytes / KB:.2f} KB"
    else:
        size = f"{size_bytes} bytes"
    
    return size
  
  def start_download(self,e:TapEvent):
    chosen_res = self.reses_group.value.upper()
    asyncio.run(self.read_write_details(self.details_fetched.get(chosen_res))) 
    
    self.reset_view()
    self.download_items_column.controls.append(DownloadItem(filename='filename',filesize='25 MB',status='Completed'))
    self.download_items_column.update()
    
  def cancelled(self,e:TapEvent):
    self.reset_view()

  def downloader(self,url):
    pass

  

  async def read_write_details(self, new_download):
    with open("data.json", "r") as f:
        downloads = json.load(f)
    downloads["downloads"].append(new_download)
    with open("data.json", "w") as f:
        json.dump(downloads, f, indent=4)

  def read_details(self):
    with open("data.json", "r") as f:
      downloads = json.load(f)['downloads']
    return downloads

  def load_history(self):
    for file in self.read_details():
      self.download_items_column.controls.append(
        DownloadItem(
          filename=file['filename'],
          filesize=file['size'],
          status='Completed',
        )
      )
      self.download_items_column.update()



app(target=Main,view=WEB_BROWSER,web_renderer='html', assets_dir='assets')