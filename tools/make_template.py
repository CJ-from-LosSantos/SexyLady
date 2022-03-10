from string import Template


def tmpl_init(d: dict):
    # filePath = '../parser_conf_test.py'

    for k, v in d.items():
        filePath = '../' + v
        class_file = open(filePath, 'w')

        mycode = []

        # 加载模板文件
        # template_file = open('../conf/isparser_tmpl.tmpl', 'r')
        template_file = open('../conf/' + k, 'r')
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
    tmpl = {"isparser_tmpl.tmpl": "parser_conf_test.py", "isspider_tmpl.tmpl": "spider_test.py"}
    tmpl_init(tmpl)
    print('Create template successfully')
