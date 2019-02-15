const fs = require('fs');
const FILE_PATH = './file-yamls/05-apache.yaml';

const readFile = filePath => {
  let returnArr = [];

  return new Promise((resolve, reject) => {
    fs.readFile(filePath, 'utf8', read = (err, data) => {
      let lines = data.toString().split("\n");
      if (err) throw err;
      for (i in lines) {
        let line = lines[i].trim();
        if ((!line.startsWith('#')) && line)
          returnArr.push(line);
      }

      resolve(returnArr);
    });
  });
}

const main = (name = 'container_identifier') => {
  readFile(FILE_PATH).then(keyVal => {
    let obj = loopThroughKeyVal(keyVal);
    console.log(`metadata:\n  name: ${name}\n  annotations:    `);
    console.log(`    ad.datadoghq.com/${name}.check_names: [${obj.check_names}]`);
    console.log(`    ad.datadoghq.com/${name}.init_configs: [${obj.init_config}]`);
    console.log(`    ad.datadoghq.com/${name}.instances: [${obj.instance_config}]`);
    console.log(`    ad.datadoghq.com/${name}.logs: [${obj.log_config}]`);
  });
}

const loopThroughKeyVal = data => {
  let jsonObj = {
    'check_names'     : [],
    'init_config'     : [],
    'instance_config' : [],
    'log_config'      : [],
  }

  let current = 'check_names';

  for (let i = 0; i < data.length; i++) {
    if (data[i] === 'init_config:') {
      current = 'init_config';
    } else if (data[i] === 'instances:') {
      current = 'instance_config';
    } else if (data[i] === 'logs:') {
      current = 'log_config';
    }

    if (data[i].startsWith('-') && current !== 'check_name') {
      let key = '"' + data[i].split(/:(.+)?/)[0].slice(2) + '"';
      let val = '"' + data[i].split(/:(.+)?/)[1].trim() + '"';
      jsonObj[current].push(` {${key}: ${val}}`);
    } else if (data[i].includes(': ')) {
      key = '"' + data[i].split(/:(.+)?/)[0] + '"';
      val = '"' + data[i].split(/:(.+)?/)[1].trim() + '"';
      jsonObj[current].push(` {${key}: ${val}} `);
    }
  }

  return jsonObj;
}

main();

/*
metadata:
  name: apache
  annotations:
    ad.datadoghq.com/<container identifier>.check_names: '[<CHECK_NAME>]'
    ad.datadoghq.com/<container identifier>.init_configs: '[<INIT_CONFIG>]'
    ad.datadoghq.com/<container identifier>.instances: '[<INSTANCE_CONFIG>]'
    ad.datadoghq.com/<container identifier>.logs: '[<LOG_CONFIG>]'

LABEL "com.datadoghq.ad.check_names"='["nginx"]'
LABEL "com.datadoghq.ad.init_configs"='[{}]'
LABEL "com.datadoghq.ad.instances"='[{"nginx_status_url": "http://%%host%%:%%port%%/nginx_status"}]'
LABEL "com.datadoghq.ad.logs"='[{"source": "nginx", "service": "webapp"}]'
*/

