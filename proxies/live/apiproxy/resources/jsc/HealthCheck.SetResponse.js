const apiproxy_revision = context.getVariable('apiproxy.revision')

const healthcheck_request_url = context.getVariable('healthcheckRequest.url')

function is_healthy(policy_name) {
  const status_code = context.getVariable(policy_name + '.status.code')
  const content = context.getVariable(policy_name + '.content')

  return status_code === 200 && JSON.parse(content)['status'] === 'pass'
}

function json_tryparse(raw) {
  try {
    return JSON.parse(raw)
  } catch (e) {
    return raw
  }
}

const PDS_healthcheck_status = is_healthy('PDShealthcheckResponse') ? 'pass' : 'fail'
const SDS_healthcheck_status = is_healthy('SDShealthcheckResponse') ? 'pass' : 'fail'
const fhir_converter_healthcheck_status = is_healthy('fhirConverterHealthcheckResponse') ? 'pass' : 'fail'

const orange_healthcheck_status_code = context.getVariable('orangeHealthcheckResponse.status.code')
const orange_healthcheck_status = (orange_healthcheck_status_code <= 500) ? 'pass' : 'fail'

const healthcheck_content = json_tryparse(context.getVariable('healthcheckResponse.content'))
const healthcheck_status_code = context.getVariable('healthcheckResponse.status.code')
const healthcheck_status = (healthcheck_status_code / 100 === 2) ? 'pass' : 'fail'
const healthcheck_failed = context.getVariable('servicecallout.ServiceCallout.CallHealthcheckEndpoint.failed')
const timeout = (healthcheck_status_code === null && healthcheck_failed) ? 'true' : 'false'

const final_status = (healthcheck_status === 'pass' &&
  PDS_healthcheck_status === 'pass' &&
  SDS_healthcheck_status === 'pass' &&
  orange_healthcheck_status === 'pass' &&
  fhir_converter_healthcheck_status === 'pass')
  ? 'pass' : 'fail'

const resp = {
  'status': final_status,
  'version': '{{ DEPLOYED_VERSION }}',
  'revision': apiproxy_revision,
  'releaseId': '{{ RELEASE_RELEASEID }}',
  'commitId': '{{ SOURCE_COMMIT_ID }}',
  'checks': {
    'healthcheck': {
      'status': healthcheck_status,
      'timeout': timeout,
      'responseCode': healthcheck_status_code,
      'outcome': healthcheck_content,
      'links': { 'self': healthcheck_request_url },
    },
    'dependencies': {
      'PDS status': PDS_healthcheck_status,
      'SDS status': SDS_healthcheck_status,
      'Orange TestLab status': orange_healthcheck_status,
      'fhir-converter status': fhir_converter_healthcheck_status,
    },
  },
}

context.setVariable('status.response', JSON.stringify(resp))
context.setVariable('response.content', JSON.stringify(resp))
context.setVariable('response.header.Content-Type', 'application/json')
