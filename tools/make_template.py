from string import Template


def tmpl_init():
    filePath = '../parser_conf_test.py'
    class_file = open(filePath, 'w')

    mycode = []

    # 加载模板文件
    template_file = open('../conf/is_tmpl.tmpl', 'r')
    tmpl = Template(template_file.read())

    # 模板替换
    mycode.append(tmpl.substitute(
        CLASSNAME='DEFAULT',
        Class_Name='Default',
        En_name='mystruct',
        Type='int',
        Name='value'))

    # 将代码写入文件
    class_file.writelines(mycode)
    class_file.close()


if __name__ == '__main__':
    tmpl_init()
    print('Create template successfully')
