# Siebel eScript memory leak analyzer tool

This tool is intended to analyze Siebel's eScript code for memory leak candidates.

It will parse all eScripts in the repository searching for variables not destroyed and Business Objects and Business Components that were not destroyed in the correct order.

Variable types evaluated for destruction:
* ActiveBusObject
* GetBusObject
* GetBusComp
* ParentBusComp
* GetService
* NewPropertySet
* GetMVGBusComp
* GetPicklistBusComp

# How to deploy

## Requirements

* AWS CLI already configured with Administrator permission
* [AWS SAM CLI installed](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) - minimum version 0.48.
* [NodeJS 12.x installed](https://nodejs.org/en/download/)

## SAM Deploy

```
sam deploy --guided
```

# How to use

Access:
https://jpmota.net/memleak


Export eScripts from your Siebel Repository by running below SQL depending on your current version:

## BEFORE IP17
```
select 'APPLET', applet.name, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_APPL_WEBSCRPT script, SIEBEL.S_APPLET applet where applet.row_id = SCRIPT.APPLET_ID and SCRIPT.REPOSITORY_ID = (select ROW_ID from siebel.s_repository where name = 'Siebel Repository') and applet.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'APPLICATION', application.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_APPL_SCRIPT script, SIEBEL.S_APPLICATION application where script.REPOSITORY_ID = (select ROW_ID from siebel.s_repository where name = 'Siebel Repository') and script.application_id = application.row_id and application.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'BUSINESS COMPONENT', BC.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_BUSCOMP_SCRIPT script, SIEBEL.S_BUSCOMP BC where script.REPOSITORY_ID = (select ROW_ID from siebel.s_repository where name = 'Siebel Repository') and bc.row_id = SCRIPT.BUSCOMP_ID and BC.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'BUSINESS SERVICE', BS.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_SERVICE_SCRPT script, SIEBEL.S_SERVICE BS where script.REPOSITORY_ID = (select ROW_ID from siebel.s_repository where name = 'Siebel Repository') and bs.row_id = SCRIPT.SERVICE_ID and BS.inactive_flg = 'N' and script.inactive_flg = 'N'
```

## AFTER IP17
```
select 'APPLET', applet.name, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_APPL_WEBSCRPT script, SIEBEL.S_APPLET applet where applet.row_id = SCRIPT.APPLET_ID and SCRIPT.REPOSITORY_ID = (select WKS.repository_id from SIEBEL.S_WORKSPACE WKS where WKS.NAME='MAIN' and WKS.REPOSITORY_ID = (select row_id from S_REPOSITORY where NAME = 'Siebel Repository')) and applet.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'APPLICATION', application.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_APPL_SCRIPT script, SIEBEL.S_APPLICATION application where script.REPOSITORY_ID = (select repository_id from SIEBEL.S_WORKSPACE where NAME='MAIN' and REPOSITORY_ID = (select row_id from SIEBEL.S_REPOSITORY where NAME = 'Siebel Repository')) and script.application_id = application.row_id and application.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'BUSINESS COMPONENT', BC.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_BUSCOMP_SCRIPT script, SIEBEL.S_BUSCOMP BC where script.REPOSITORY_ID = (select repository_id from SIEBEL.S_WORKSPACE where NAME='MAIN' and REPOSITORY_ID = (select row_id from SIEBEL.S_REPOSITORY where NAME = 'Siebel Repository')) and bc.row_id = SCRIPT.BUSCOMP_ID and BC.inactive_flg = 'N' and script.inactive_flg = 'N' UNION ALL
select 'BUSINESS SERVICE', BS.NAME, script.created, script.created_by, script.last_upd, script.last_upd_by, script.name, script.script from SIEBEL.S_SERVICE_SCRPT script, SIEBEL.S_SERVICE BS where script.REPOSITORY_ID = (select repository_id from SIEBEL.S_WORKSPACE where NAME='MAIN' and REPOSITORY_ID = (select row_id from SIEBEL.S_REPOSITORY where NAME = 'Siebel Repository')) and bs.row_id = SCRIPT.SERVICE_ID and BS.inactive_flg = 'N' and script.inactive_flg = 'N'
```

# Contributing

Contributions are welcome! If you'd like to contribute, please share your ideas. Pull requests are warmly welcome.


# Author

**João Paulo de Matos Mota** - [Github Account](https://github.com/jpmmota)


## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/jpmmota/escriptmemleakanalyzer/blob/master/LICENSE) file for details
