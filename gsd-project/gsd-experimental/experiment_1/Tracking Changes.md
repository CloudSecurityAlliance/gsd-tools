Don't do this:

```json
{
	"GSD-ID": "GSD-2021-1234567"
	"CHANGE_LOG": {
		"id": "GSD-2021-1234567",
		"changes": [
			{
				"OLD": {},
				"NEW": {},
				"CHANGED_BY": {},
				"TIMESTAMP": ""
			}
		]
	}
}
```

For now we'll rely entirely on Git for version control/history/blame related data. Long term we don't want to cement ourselves within Git, but it serves our needs for now.