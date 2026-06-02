'use client'

import { useState } from 'react'
import { createBrowserClient } from '@supabase/ssr'

export default function ProfileForm({ user }: any) {

  const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )

  const [name, setName] = useState(user.user_metadata?.name || '')
  const [password, setPassword] = useState('')
  const [avatar, setAvatar] = useState<File | null>(null)
  const [message, setMessage] = useState('')

  const updateProfile = async () => {

    const { error } = await supabase.auth.updateUser({
      data: { name }
    })

    if (error) setMessage(error.message)
    else setMessage("Profile updated")
  }

  const updatePassword = async () => {

    const { error } = await supabase.auth.updateUser({
      password
    })

    if (error) setMessage(error.message)
    else {
      setPassword('')
      setMessage("Password updated")
    }
  }

  const uploadAvatar = async () => {

    if (!avatar) return

    const filePath = `${user.id}/${avatar.name}`

    const { error } = await supabase.storage
      .from('avatars')
      .upload(filePath, avatar, { upsert: true })

    if (error) {
      setMessage(error.message)
      return
    }

    const { data } = supabase
      .storage
      .from('avatars')
      .getPublicUrl(filePath)

    await supabase.auth.updateUser({
      data: { avatar_url: data.publicUrl }
    })

    setMessage("Avatar updated")
  }

  return (
    <div className="space-y-6">

      {/* NAME */}
      <div>
        <label className="text-sm">Name</label>

        <input
          className="w-full border rounded px-3 py-2 mt-1"
          value={name}
          onChange={(e)=>setName(e.target.value)}
        />

        <button
          onClick={updateProfile}
          className="mt-2 w-full bg-black text-white py-2 rounded"
        >
          Save Profile
        </button>
      </div>


      {/* EMAIL */}
      <div>
        <label className="text-sm">Email</label>

        <input
          disabled
          value={user.email}
          className="w-full border rounded px-3 py-2 mt-1 bg-gray-100"
        />
      </div>


      {/* PASSWORD */}
      <div>
        <label className="text-sm">New Password</label>

        <input
          type="password"
          className="w-full border rounded px-3 py-2 mt-1"
          value={password}
          onChange={(e)=>setPassword(e.target.value)}
        />

        <button
          onClick={updatePassword}
          className="mt-2 w-full bg-black text-white py-2 rounded"
        >
          Change Password
        </button>
      </div>


      {/* AVATAR */}
      <div>

        <label className="text-sm">Avatar</label>

        <input
          type="file"
          onChange={(e)=>setAvatar(e.target.files?.[0] || null)}
          className="mt-1"
        />

        <button
          onClick={uploadAvatar}
          className="mt-2 w-full bg-black text-white py-2 rounded"
        >
          Upload Avatar
        </button>

      </div>

      {message && (
        <p className="text-center text-sm">
          {message}
        </p>
      )}

    </div>
  )
}