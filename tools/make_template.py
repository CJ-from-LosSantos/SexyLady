from string import Template


def tmpl_init(d: dict):
    # filePath = '../parser_conf_test.py'

    for k, v in d.items():
        filePath = '../tmpl/' + v
        class_file = open(filePath, 'w', encoding='utf-8')

        mycode = []

        # 加载模板文件
        # template_file = open('../conf/isparser_tmpl.tmpl', 'r')
        template_file = open('../conf/' + k, 'r', encoding='utf-8')
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
    tmpl = {"isyaml.tmpl": "first_job.yaml", "isspider.tmpl": "set_spiders.py"}
    tmpl_init(tmpl)
    print('Create template successfully')
