# yezihangism
for my own website

模型类的字段会映射到数据库表的字段。表单类的字段会映射到html中<input>标签元素

当我们在视图中处理模型实例时，我们一般从数据库中获取它。当我们处理表单时，我们一般在视图中实例化它。
当我们实例化表单时，我们可以选择让它为空或者对它预先填充，例如使用：
  1. 来自已保存的模型实例的数据（例如在管理编辑表单的情况下）
  2. 我们从其他来源获取的数据
  3. 从前面一个HTML 表单提交过来的数据
最后一种情况最有趣，因为这使得用户不仅可以阅读网站，而且还可以将信息发回给它。

当我们使用编辑类视图——例如CreateView——等，我们需要在mmodels中定义get_absolute_url()方法。这是因为通用视图在对一个对象完成编辑后，需要一个返回链接。

展示类视图中
    
    model = Model
就相当于

    model = Model.objects.get()
至于是get()，或者all()，取决于你的类视图继承自哪个父类视图

form类的运行顺序为: init, clean, validate, save，
运行forms.is_valid()时一次调用clean和validate
is_valid()判断为True后，如果入库出现问题，就不能再将错误信息封装到form的错误结构中

is_authenticated可以检查用户是否经过验证，但考虑这样的场景：
  1. 希望导航栏可以根据是否经过验证来展示登录或者登出（只能同时展示一个选项）
  2. 一个侧边栏选项用于展示所有用户的列表，并且可以通过选择用户跳转到对应的用户详情页面
  3. 进入用户详情页面并不表示该用户已经登录，但是导航栏会做出用户已经登录的反应，展示登录后才展示的选项（登出）
  
is_authenticated并不意味着任何权限，也不会检查用户是否处于活动状态或是否具有有效会话。
即使通常你会在request.user上检查这个属性，以确定它是否已被AuthenticationMiddleware（代表当前登录的用户）填充，你应该知道任何User实例的这个属性为True。

尽量不使用原有的User模型，有两种方法可以扩展User模型
  1. 如果你需要改变的只是行为，并且不需要改变数据库存储的内容，那么你可以建立一个基于User模型的代理模型。它允许代理模型提供很多功能，包括默认排序，自定    义的管理器和自定义的模型方法等。
     如果你想存储与User模型关联的信息，可以使用OneToOneField到包含其他信息字段的模型。这种one-to-one模型经常被称作Profile模型，因为它可能存储站点用    户的非身份验证的相关信息。
  2. 设置一个自定义的用户模型，继承自AbstractUser
  
重写save_models方法能够在后台实现某些功能，例如在保存博客信息时自动添加作者。

filter()可以指定多个参数，参数间会以and连接形成sql的where条件语句
filter()中参数一般指定字段名，例如id。对于字段的查询方式，可以在该字段名后加上特定后缀：
  1. id__exact == ... where id = xxx
  2. id__contain == ... where id like xxx
  3. id__gte == ... where id >= xxx
  4. id__startswith == ... where id like xxx%
  5. id__year == ... where id between 2005-1-1 and 2005-12-31
多个查询方式可以组合在一起，如id__year__gte

图片过长，超出了div盒子的范围可以通过在css文件中设置img标签的属性控制
    
    p img {
        width: auto;
        ...
    }
  
点击图片显示未压缩的原始图片功能
  
  
get_next_in_order(): 获取当前对象的下一个对象
get_previous_in_order(): 获取当前对象的上一个对象

在定义order_with_respect_to之后可使用。

    obj = Model.objects.get(id=3)
    obj.get_next_in_order()  # 4

box-shadow属性：如果设置padding，那么阴影将出现在padding边缘，如果设置margin，阴影位置不变
  
Django的静态文件配置：
  1. 设置STATIC_URL,STATIC_ROOT,MEDIA_URL,MEDIA_ROOT
  2. 在模板中引用。
    
    {% load static %}
    {% static 'path/to/static.jpg' %}
    
  3. 将静态文件保存至static目录中。注意：在开发环境下。如果你使用 django.contrib.staticfiles。那么当你在DEBUG为True时运行runserver，django将自动为你保存静态文件。
  这种方法不可以使用到生产环境中。
  4. 在生产环境中，运行collectstatic 将所需的所有静态文件复制到根据你的STATIC_ROOT得到的相对路径中去。
    
    $ python manage.py collectstatic
    
django-ckeditor
  1. https://github.com/django-ckeditor/django-ckeditor
  
  
搜索结果如果要做分页的话，不能简单地和展示分页一样，因为url中会带有参数

    search/?csrfmiddlewaretoken=oK8dulv7rKs7LVVtPZjQHhjmk1u9ZxtJM9fX43oyKKel719bfyPIdO4dPIfBDJVd&search=关键词
   
如果要做分页，那么不能和主页的分页展示共用一个模板，两者的路径是不同的。
函数视图中使用分页可参考  https://github.com/django/django/blob/master/django/views/generic/list.py
  
对于导航栏上的专题分类，可以考虑将其列为一个单独的模型，这样做的好处是，不同专题的博客享用不同的id，跳转到上一篇或下一篇时不会混淆。缺点是包含拥有Blog外键的模型——例如comment——都要新增一个。

毫无疑问两个模型会有许多相同的字段和方法，对于相同的方法——例如display_tag——可以这样抽象：

创建一个继承自 django.db.models.Manager 的类

    class BaseManager(models.Manager):
        
        def method(self, keyword):
            return self.filter(field__option = keyword)
            
在需要用到这个方法的模型中调用该类：

    class Blog(models.Model):
        title = CharField()
        authors = CharField()
        ...
        objects = BaseManager()
        
        def __str__(self):
            return self.xxx
     
objects用于取代模型默认的manager（objects），这样，我们就可以使用该方法：
    
    Blog.objects.method("django")
    
与下面的代码等同

    Blog.objects.filter(title__icontains="django")

或者使用外键的形式，每一篇博客都有一个唯一的专题id。主要的问题在于如何从主页上获取某一专题的id，也就是说，如何让数据库中存储的专题展示在导航栏上，而不是自己手动写上去（因为这样做无法和数据库中保存的专题联系起来，也就得不到id）。
另外这个方法无法通过在models中增加方法来返回所有数据。还是需要该模型当前的id

或者，类似博客列表，通过点击导航栏上给定的选项去展示专题列表，通过点击不同的专题展示该专题下的所有博客。但是同样的问题——id的跳转问题——依旧存在。

留言功能，评论功能，需要登录权限，需要开放注册页面。

博客浏览量自增。类视图中重写get_object()函数，获取相应blog，blog浏览量字段+=1，再保存

排序条件：日期倒序、浏览量倒序

UI重做，去除评论、登录、注册功能。新增给我留言功能，管理员可见
