import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import SearchPanel from '../SearchPanel.vue'

describe('SearchPanel', () => {
  it('emits query event with code', async () => {
    const wrapper = mount(SearchPanel)
    await wrapper.find('input[placeholder="请输入股票代码"]').setValue('000001')
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted().query).toBeTruthy()
    expect(wrapper.emitted().query[0]).toEqual([{ stock_code: '000001' }])
  })

  it('emits query event with name', async () => {
    const wrapper = mount(SearchPanel)
    await wrapper.find('input[placeholder="请输入股票名称（支持模糊查询）"]').setValue('平安银行')
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted().query).toBeTruthy()
    expect(wrapper.emitted().query[0]).toEqual([{ stock_name: '平安银行' }])
  })

  it('disables query button when inputs are empty', () => {
    const wrapper = mount(SearchPanel)
    const button = wrapper.find('button')
    expect(button.attributes('disabled')).toBeDefined()
  })
})
