import { describe, it, expect } from 'vitest'

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i

function formatUUID(chars: string[]): string {
  const value = chars.join('')
  return [value.slice(0, 8), value.slice(8, 12), value.slice(12, 16), value.slice(16, 20), value.slice(20, 32)]
    .filter(Boolean)
    .join('-')
}

function isValidUUID(chars: string[]): boolean {
  if (chars.some(c => c === '')) return false
  return UUID_REGEX.test(formatUUID(chars))
}

describe('UUID utilities', () => {
  describe('formatUUID', () => {
    it('formats 32 hex chars into UUID format', () => {
      const chars = '12345678901234567890123456789012'.split('')
      expect(formatUUID(chars)).toBe('12345678-9012-3456-7890-123456789012')
    })

    it('handles partial input', () => {
      const chars = '12345678'.split('').concat(Array(24).fill(''))
      expect(formatUUID(chars)).toBe('12345678')
    })

    it('handles empty input', () => {
      const chars = Array(32).fill('')
      expect(formatUUID(chars)).toBe('')
    })

    it('filters empty segments', () => {
      const chars = 'abcdef12'.split('').concat(Array(24).fill(''))
      expect(formatUUID(chars)).toBe('abcdef12')
    })
  })

  describe('isValidUUID', () => {
    it('validates correct UUID format', () => {
      const chars = '12345678-9012-3456-7890-123456789012'.replace(/-/g, '').split('')
      expect(isValidUUID(chars)).toBe(true)
    })

    it('rejects incomplete UUID', () => {
      const chars = Array(31).fill('1').concat([''])
      expect(isValidUUID(chars)).toBe(false)
    })

    it('rejects UUID with missing segments', () => {
      const chars = '12345678901234567890123456789'.split('').concat([''])
      expect(isValidUUID(chars)).toBe(false)
    })

    it('rejects UUID with invalid characters', () => {
      const chars = '1234567890123456789012345678901g'.split('')
      expect(isValidUUID(chars)).toBe(false)
    })

    it('accepts lowercase hex', () => {
      const chars = 'abcdef0123456789abcdef0123456789'.split('')
      expect(isValidUUID(chars)).toBe(true)
    })

    it('accepts uppercase hex', () => {
      const chars = 'ABCDEF0123456789ABCDEF0123456789'.split('')
      expect(isValidUUID(chars)).toBe(true)
    })
  })
})
