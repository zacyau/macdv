import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import IndicatorCards from '../IndicatorCards.vue'

describe('IndicatorCards', () => {
  it('renders data correctly', () => {
    const data = {
      current_price: 10.5,
      macdv: 1.23,
      rsi14: 75,
      macdv_trend: 'up',
      rsi14_signal: 'overbought'
    }
    const wrapper = mount(IndicatorCards, { props: { data } })
    expect(wrapper.text()).toContain('10.5')
    expect(wrapper.text()).toContain('1.23')
    expect(wrapper.text()).toContain('75')
    expect(wrapper.text()).toContain('上升')
    expect(wrapper.text()).toContain('超买')
  })
})
