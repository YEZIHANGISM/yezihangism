# yezihangism
for my own website

模型类的字段会映射到数据库表的字段。表单类的字段会映射到html中<input>标签元素

当我们在视图中处理模型实例时，我们一般从数据库中获取它。当我们处理表单时，我们一般在视图中实例化它。
当我们实例化表单时，我们可以选择让它为空或者对它预先填充，例如使用：
  1. 来自已保存的模型实例的数据（例如在管理编辑表单的情况下）
  2. 我们从其他来源获取的数据
  3. 从前面一个HTML 表单提交过来的数据
最后一种情况最有趣，因为这使得用户不仅可以阅读网站，而且还可以将信息发回给它。

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


  
Django的静态文件配置：
  1. 设置STATIC_URL
  2. 在模板中引用。
    
    {% load static %}
    {% static 'path/to/static.jpg' %}
    
  2. 将静态文件保存至static目录中。注意：在开发环境下。如果你使用 django.contrib.staticfiles。那么当你在DEBUG为True时运行runserver，django将自动为你保存静态文件。
  这种方法不可以使用到生产环境中。
  
